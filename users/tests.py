from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserAuthTests(APITestCase):
    def test_register_success(self):
        url = reverse("register")
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "password_confirmation": "password123",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_password_mismatch(self):
        url = reverse("register")
        payload = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "password123",
            "password_confirmation": "different123",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="testuser2").exists())

    def test_login_token_obtain(self):
        User.objects.create_user(
            username="loginuser",
            email="loginuser@example.com",
            password="password123",
        )
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url,
            {"username": "loginuser", "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
