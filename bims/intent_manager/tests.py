from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class IntentManagerTests(APITestCase):
    client = APIClient
    url = '/api/intents/'
    token = None

    def setUp(self) -> None:
        """obtain a valid token"""
        credentials = {'username': 'testUser0',
                       'password': 'password'}
        self.token = self.client.post('/api/auth/register', credentials, format='json').data.get('token')

    def test_get_intents_unauthorized(self):
        """tests GET request without a token, expects a 401 status code"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_intents(self):
        """tests GET request with token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
