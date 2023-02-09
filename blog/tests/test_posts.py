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
