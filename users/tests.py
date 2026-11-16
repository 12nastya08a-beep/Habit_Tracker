import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_register_success(api_client):
    url = reverse("register")
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "password_confirmation": "password123",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_register_password_mismatch(api_client):
    url = reverse("register")
    payload = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "password123",
        "password_confirmation": "different123",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not User.objects.filter(username="testuser2").exists()


@pytest.mark.django_db
def test_login_token_obtain(api_client):
    User.objects.create_user(
        username="loginuser",
        email="loginuser@example.com",
        password="password123",
    )
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url,
        {"username": "loginuser", "password": "password123"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
