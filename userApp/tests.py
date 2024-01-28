# Import necessary modules
from rest_framework.test import APITestCase
from rest_framework import status
from userApp.models import ApplicationUser
from django.urls import reverse


class YourApiTestCase(APITestCase):
    def setUp(self):
        self.user = ApplicationUser.objects.create_user(
            email="maulik@gmail.com", password="1234"
        )
        self.token = None

    def test_login_positive(self):
        # Define your API endpoint URL
        url = "/user/auth/login/"  # Replace with your actual API endpoint name
        data = {
            "email": "maulik@gmail.com",
            "password": "1234",
            # Add more fields as needed
        }

        # Example headers
        headers = {
            "API-KEY": "gAAAAABjBwBkkGqfJejIn9GHxzWXNjUA-rSNgd6e7xJFeImboBJ-F8weNwVtGjqO2LcMd9obyWTtHxgXgG8sz36g9n8tjtbC5o8ygMDZ_hxZhfjeIdvG8ss=",
            "Content-Type": "application/json",
            # Add more headers as needed
        }

        # Example: Making a GET request
        response = self.client.post(
            url, data, format="json", HTTP_API_KEY=headers["API-KEY"]
        )
        self.token = response.data.get("X-Token")
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_negative_not_send_password(self):
        # Define your API endpoint URL
        url = "/user/auth/login/"  # Replace with your actual API endpoint name
        data = {
            "email": "maulik@gmail.com",
            # Add more fields as needed
        }
        # Example headers
        headers = {
            "API-KEY": "gAAAAABjBwBkkGqfJejIn9GHxzWXNjUA-rSNgd6e7xJFeImboBJ-F8weNwVtGjqO2LcMd9obyWTtHxgXgG8sz36g9n8tjtbC5o8ygMDZ_hxZhfjeIdvG8ss=",
            "Content-Type": "application/json",
            # Add more headers as needed
        }
        # Example: Making a GET request
        response = self.client.post(
            url, data, format="json", HTTP_API_KEY=headers["API-KEY"]
        )
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
