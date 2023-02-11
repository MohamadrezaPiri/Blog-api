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
