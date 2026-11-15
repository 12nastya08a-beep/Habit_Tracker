from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Habit, HabitLog


class HabitApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="habituser",
            email="habituser@example.com",
            password="password123",
        )
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            title="Читання",
            description="30 хвилин щодня",
        )

    def test_list_habits(self):
        url = reverse("habit-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_habit_success(self):
        url = reverse("habit-list-create")
        response = self.client.post(
            url,
            {"title": "Біг", "description": "20 хвилин"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.filter(title="Біг").exists())

    def test_create_habit_invalid(self):
        url = reverse("habit-list-create")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_detail_get_and_patch(self):
        url = reverse("habit-detail", kwargs={"pk": self.habit.pk})
        get_resp = self.client.get(url)
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)

        patch_resp = self.client.patch(
            url,
            {"title": "Читання ввечері"},
            format="json",
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.title, "Читання ввечері")

    def test_delete_habit_blocked_when_logs_exist(self):
        HabitLog.objects.create(
            habit=self.habit,
            date="2026-11-15",
            is_completed=True,
        )
        url = reverse("habit-detail", kwargs={"pk": self.habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Habit.objects.filter(pk=self.habit.pk).exists())

    def test_delete_habit_success(self):
        url = reverse("habit-detail", kwargs={"pk": self.habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())

    def test_delete_habit_not_found(self):
        url = reverse("habit-detail", kwargs={"pk": 99999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_model_str(self):
        log = HabitLog.objects.create(
            habit=self.habit,
            date="2026-11-15",
            is_completed=True,
        )
        self.assertEqual(str(self.habit), "Читання")
        self.assertIn("Читання", str(log))
        self.assertIn("Виконано", str(log))

    def test_patch_habit_invalid(self):
        url = reverse("habit-detail", kwargs={"pk": self.habit.pk})
        response = self.client.patch(url, {"title": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("habit-list-create")
        response = self.client.post(
            url,
            {"title": "Без токена", "description": "Тест"},
            format="json",
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
