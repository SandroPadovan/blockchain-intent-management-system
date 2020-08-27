from rest_framework import status
from rest_framework.test import APITestCase
from user_manager.models import User


class UserManagerTests(APITestCase):

    url = '/api/auth/register'

    def test_register_user(self):
        """tests user creation and registration"""

        data = {'username': 'testUser0',
                'password': 'password'}

        response = self.client.post(self.url, data, format='json')
        print(response.data.get('token'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testUser0')
