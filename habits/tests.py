import pytest
from django.urls import reverse
from rest_framework import status

from .models import Habit, HabitLog


@pytest.mark.django_db
def test_list_habits(auth_client, habit):
    url = reverse("habit-list-create")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_habit_success(auth_client):
    url = reverse("habit-list-create")
    response = auth_client.post(
        url,
        {"title": "Біг", "description": "20 хвилин"},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Habit.objects.filter(title="Біг").exists()


@pytest.mark.django_db
def test_create_habit_invalid(auth_client):
    url = reverse("habit-list-create")
    response = auth_client.post(url, {}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_habit_detail_get_and_patch(auth_client, habit):
    url = reverse("habit-detail", kwargs={"pk": habit.pk})
    get_resp = auth_client.get(url)
    assert get_resp.status_code == status.HTTP_200_OK

    patch_resp = auth_client.patch(
        url,
        {"title": "Читання ввечері"},
        format="json",
    )
    assert patch_resp.status_code == status.HTTP_200_OK
    habit.refresh_from_db()
    assert habit.title == "Читання ввечері"


@pytest.mark.django_db
def test_delete_habit_blocked_when_logs_exist(auth_client, habit):
    HabitLog.objects.create(
        habit=habit,
        date="2026-11-15",
        is_completed=True,
    )
    url = reverse("habit-detail", kwargs={"pk": habit.pk})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Habit.objects.filter(pk=habit.pk).exists()


@pytest.mark.django_db
def test_delete_habit_success(auth_client, habit):
    url = reverse("habit-detail", kwargs={"pk": habit.pk})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Habit.objects.filter(pk=habit.pk).exists()


@pytest.mark.django_db
def test_delete_habit_not_found(auth_client):
    url = reverse("habit-detail", kwargs={"pk": 99999})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_model_str(habit):
    log = HabitLog.objects.create(
        habit=habit,
        date="2026-11-15",
        is_completed=True,
    )
    assert str(habit) == "Читання"
    assert "Читання" in str(log)
    assert "Виконано" in str(log)


@pytest.mark.django_db
def test_patch_habit_invalid(auth_client, habit):
    url = reverse("habit-detail", kwargs={"pk": habit.pk})
    response = auth_client.patch(url, {"title": ""}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_habit_unauthenticated(api_client):
    url = reverse("habit-list-create")
    response = api_client.post(
        url,
        {"title": "Без токена", "description": "Тест"},
        format="json",
    )
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


@pytest.mark.django_db
def test_get_habit_not_found(auth_client):
    url = reverse("habit-detail", kwargs={"pk": 99999})
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
