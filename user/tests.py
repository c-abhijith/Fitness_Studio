from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserAuthTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
            role=CustomUser.Roles.USER,
            timezone="UTC"
        )

    def test_register_user_success(self):
        url = reverse('register')  
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123",
            "role": CustomUser.Roles.USER,
            "timezone": "UTC"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User registered", response.data.get('message', ''))

    def test_register_user_missing_timezone(self):
        url = reverse('register')
        data = {
            "username": "user2",
            "email": "user2@example.com",
            "password": "pass123",
            "role": CustomUser.Roles.USER,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Timezone is required for users", response.data.get('message', ''))

    def test_register_instructor_default_timezone(self):
        url = reverse('register')
        data = {
            "username": "instructor1",
            "email": "instructor@example.com",
            "password": "pass123",
            "role": CustomUser.Roles.INSTRUCTOR,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User registered", response.data.get('message', ''))

        user = CustomUser.objects.get(username="instructor1")
        self.assertEqual(user.timezone, "Asia/Kolkata")

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair') 
        data = {
            "username": self.user.username,
            "password": "testpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout_success(self):
        url = reverse('logout')  
        refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh)}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Logout successful", response.data.get('message', ''))

    def test_logout_missing_refresh_token(self):
        url = reverse('logout')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Refresh token is required", response.data.get('message', ''))
