import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from habits.models import Habit


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="habituser",
        email="habituser@example.com",
        password="password123",
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def habit(user):
    return Habit.objects.create(
        user=user,
        title="Читання",
        description="30 хвилин щодня",
    )
