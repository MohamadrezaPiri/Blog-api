import pytest
from django.contrib.auth.models import User
from rest_framework import status
from model_bakery import baker
from blog.models import Post


# FIXTURES
@pytest.fixture
def create_post(api_client):
    def do_create_post(post):
        return api_client.post('/posts/', post)
    return do_create_post


@pytest.fixture
def update_post(api_client):
    def do_update_post(post_id, post):
        return api_client.put(f'/posts/{post_id}/', post)
    return do_update_post


@pytest.fixture
def delete_post(api_client):
    def do_delete_post(post_id):
        return api_client.delete(f'/posts/{post_id}/')
    return do_delete_post


@pytest.fixture
def retrieve_post(api_client):
    def do_retrieve_post(post_id):
        return api_client.get(f'/posts/{post_id}/')
    return do_retrieve_post


# TESTS
@pytest.mark.django_db
class TestCreatePost:
    def test_if_user_is_anonymus_returns_401(self, create_post):
        response = create_post({'title': 'a', 'content': 'aa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_title_is_invalid_returns_401(self, create_post, authenticate):
        user = baker.make(User)

        authenticate(user=user)
        response = create_post({'title': '', 'content': 'aa'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_content_is_invalid_returns_401(self, create_post, authenticate):
        user = baker.make(User)

        authenticate(user=user)
        response = create_post({'title': 'a', 'content': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_post, authenticate):
        user = baker.make(User)

        authenticate(user=user)
        response = create_post({'title': 'a', 'content': 'aa'})

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUpdatePost:
    def test_if_title_is_invalid_returns_400(self, authenticate, update_post):
        user = baker.make(User)
        post = baker.make(Post, user=user)

        authenticate(user=user)
        response = update_post(
            post.id, {'title': '', 'content': post.content})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_content_is_invalid_returns_400(self, authenticate, update_post):
        user = baker.make(User)
        post = baker.make(Post, user=user)

        authenticate(user=user)
        response = update_post(
            post.id, {'title': post.title, 'content': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_anonymus_returns_401(self, update_post):
        post = baker.make(Post)

        response = update_post(
            post.id, {'title': post.title, 'content': post.content})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(self, authenticate, update_post):
        author = baker.make(User)
        user = baker.make(User)
        post = baker.make(Post, user=author)

        authenticate(user=user)
        response = update_post(
            post.id, {'title': post.title, 'content': post.content})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_200(self, authenticate, update_post):
        author = baker.make(User)
        post = baker.make(Post, user=author)

        authenticate(user=author)
        response = update_post(
            post.id, {'title': post.title, 'content': post.content})

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, authenticate, update_post):
        author = baker.make(User)
        admin = baker.make(User, is_staff=True)
        post = baker.make(Post, user=author)

        authenticate(user=admin)
        response = update_post(
            post.id, {'title': post.title, 'content': post.content})

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeletePost:
    def test_if_user_is_anonymous_returns_401(self, delete_post):
        post = baker.make(Post)

        response = delete_post(post.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(self, authenticate, delete_post):
        author = baker.make(User)
        user = baker.make(User)
        post = baker.make(Post, user=author)

        authenticate(user=user)
        response = delete_post(post.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_204(self, authenticate, delete_post):
        author = baker.make(User)
        post = baker.make(Post, user=author)

        authenticate(user=author)
        response = delete_post(post.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_admin_returns_204(self, authenticate, delete_post):
        author = baker.make(User)
        admin = baker.make(User, is_staff=True)
        post = baker.make(Post, user=author)

        authenticate(user=admin)
        response = delete_post(post.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestRetrievePost:
    def test_if_post_exists_returns_200(self, retrieve_post):
        post = baker.make(Post)

        response = retrieve_post(post.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_post_does_not_exist_returns_404(self, retrieve_post):
        response = retrieve_post('1')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestGetPostsList:
    def test_if_returns_200(self, api_client):
        response = api_client.get('/posts/')

        assert response.status_code == status.HTTP_200_OK
