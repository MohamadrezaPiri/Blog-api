import pytest
from django.contrib.auth.models import User
from rest_framework import status
from model_bakery import baker
from blog.models import Post, Comment


# FIXTURES
@pytest.fixture
def create_comment(api_client):
    def do_create_comment(post_id, comment):
        return api_client.post(f'/posts/{post_id}/comments/', comment)
    return do_create_comment


@pytest.fixture
def Update_comment(api_client):
    def do_update_coment(post_id, comment_id, comment):
        return api_client.put(f'/posts/{post_id}/comments/{comment_id}/', comment)
    return do_update_coment


@pytest.fixture
def delete_comment(api_client):
    def do_delete_coment(post_id, comment_id):
        return api_client.delete(f'/posts/{post_id}/comments/{comment_id}/')
    return do_delete_coment


# TESTS
@pytest.mark.django_db
class TestCreateComment:
    def test_if_user_is_anonymous_returns_401(self, create_comment):
        post = baker.make(Post)

        response = create_comment(
            post.id, {'description': 'aaa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, create_comment, authenticate):
        post = baker.make(Post)

        authenticate()
        response = create_comment(post.id, {'description': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_comment, authenticate):
        post = baker.make(Post)
        user = baker.make(User)

        authenticate(user=user)
        response = create_comment(post.id, {'description': 'aaa'})

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUpdateComment:
    def test_if_user_is_anonymous_returns_401(self, Update_comment):
        post = baker.make(Post)
        comment = baker.make(Comment, post=post)

        response = Update_comment(post.id, comment.id, {'description': 'aaa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_not_valid_returns_400(self, Update_comment, authenticate):
        author = baker.make(User, username='Author')
        post = baker.make(Post, user=author)
        comment = baker.make(Comment, post=post, user=author)

        authenticate(user=author)
        response = Update_comment(post.id, comment.id, {'description': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_not_author_returns_403(self, Update_comment, authenticate):
        author = baker.make(User, username='Author')
        user = baker.make(User)
        post = baker.make(Post, user=author)
        comment = baker.make(Comment, post=post, user=author)

        authenticate(user=user)
        response = Update_comment(post.id, comment.id, {'description': 'aaa'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_200(self, Update_comment, authenticate):
        author = baker.make(User, username='Author')
        post = baker.make(Post, user=author)
        comment = baker.make(Comment, post=post, user=author)

        authenticate(user=author)
        response = Update_comment(post.id, comment.id, {'description': 'aaa'})

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_returns_200(self, Update_comment, authenticate):
        author = baker.make(User, username='Author')
        user = baker.make(User, is_staff=True)
        post = baker.make(Post, user=author)
        comment = baker.make(Comment, post=post, user=author)

        authenticate(user=user)
        response = Update_comment(post.id, comment.id, {'description': 'aaa'})

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteComment:
    def test_if_user_is_anonymous_returns_401(self, delete_comment):
        response = delete_comment(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(self, delete_comment, authenticate):
        author = baker.make(User, username='Author')
        user = baker.make(User)
        comment = baker.make(Comment, user=author)

        authenticate(user=user)
        response = delete_comment(comment.post.id, comment.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_author_returns_204(self, delete_comment, authenticate):
        author = baker.make(User, username='Author')
        comment = baker.make(Comment, user=author)

        authenticate(user=author)
        response = delete_comment(comment.post.id, comment.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_admin_returns_204(self, delete_comment, authenticate):
        author = baker.make(User, username='Author')
        admin = baker.make(User, is_staff=True)
        comment = baker.make(Comment, user=author)

        authenticate(user=admin)
        response = delete_comment(comment.post.id, comment.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestGetCommentsList:
    def test_if_returns_200(self, api_client):
        comment = baker.make(Comment)

        response = api_client.get(f'/posts/{comment.post.id}/comments/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_post_or_comment_does_not_exist_returns_404(self, api_client):
        response = api_client.get('/posts/1/comments/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
