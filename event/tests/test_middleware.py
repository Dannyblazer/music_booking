from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from account.tests.factories import UserFactory
import logging
from io import StringIO

class MiddlewareTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        # Ensure the token is correctly applied
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.log_output = StringIO()
        logging.getLogger('').addHandler(logging.StreamHandler(self.log_output))

    def test_request_logging(self):
        print(f"User: {self.user.username}")
        print(f"Token: {self.client.credentials()}")
        response = self.client.get('/api/events/')
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_content = self.log_output.getvalue()
        print(f"Log content: {log_content}")
        self.assertIn(f"Request: GET /api/events/ by {self.user.username}", log_content)
        self.assertIn("Response: 200", log_content)