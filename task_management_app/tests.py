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
        self.token = self.user.user_auth_tokens.create().key
        self.user1 = ApplicationUser.objects.create(
            email="maulik12@gmail.com", password="1234"
        )

    def test_create_task_positive(self):
        # Define your API endpoint URL
        url = "/task/tasks/"  # Replace with your actual API endpoint name
        data = {
            "due_date": "2024-01-01",
            "title": "test2",
            "description": "shcishcisuncis",
            "priority": "low",
            "completion_status": False,
            "is_private": False,
            "assign_user": [self.user.id, self.user1.id]
            # Add more fields as needed
        }

        # Example headers
        headers = {
            "API-KEY": "gAAAAABjBwBkkGqfJejIn9GHxzWXNjUA-rSNgd6e7xJFeImboBJ-F8weNwVtGjqO2LcMd9obyWTtHxgXgG8sz36g9n8tjtbC5o8ygMDZ_hxZhfjeIdvG8ss=",
            "Content-Type": "application/json"
            # Add more headers as needed
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        # Example: Making a GET request
        response = self.client.post(
            url, data, format="json", HTTP_API_KEY=headers["API-KEY"], **headers
        )
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
