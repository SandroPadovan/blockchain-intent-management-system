from rest_framework import status
from rest_framework.test import APITestCase
from user_manager.models import User


class UserManagerTests(APITestCase):

    def test_register_user(self):
        """tests user creation and registration"""

        url = '/api/auth/register'
        data = {'username': 'testUser0',
                'password': 'password'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Incorrect status code')
        self.assertEqual(User.objects.count(), 1, 'Wrong number of users in database')
        self.assertEqual(User.objects.get().username, 'testUser0', 'Wrong username in database')

    def test_login_user_with_correct_credentials(self):

        url = '/api/auth/login'
        user = User.objects.create_user('testUser1', None, 'password')
        user.save()

        data = {'username': 'testUser1',
                'password': 'password'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertEqual(response.data.get('user').get('username'), 'testUser1', 'Wrong username in response')
        self.assertIsNotNone(response.data.get('token'), 'No token was sent in response')

    def test_login_user_with_incorrect_credentials(self):

        url = '/api/auth/login'
        user = User.objects.create_user('testUser2', None, 'password')
        user.save()

        data = {'username': 'testUser2',
                'password': 'wrongPassword'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Incorrect status code')
        self.assertIsNotNone(response.data.get('non_field_errors'), 'Response did not contain non_field_errors')

    def test_logout_user(self):

        # Set up: login user
        user = User.objects.create_user('testUser3', None, 'password')
        user.save()
        data = {'username': 'testUser3',
                'password': 'password'}
        response = self.client.post('/api/auth/login', data, format='json')
        token = response.data.get('token')

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Login: Incorrect status code')
        self.assertIsNotNone(token, 'No token was sent in login response')

        # make logout request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/api/auth/logout', None)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Incorrect status code')

        # make a request to see if token is not valid anymore
        test_response = self.client.get('/api/intents/')

        self.assertEqual(test_response.status_code, status.HTTP_401_UNAUTHORIZED, 'Test-request: Incorrect status code')
        self.assertEqual(test_response.data.get('detail'), 'Invalid token.',
                         'Detail in response does not match the expected.')

    def test_get_user(self):

        # set up: register user to get valid token
        data = {'username': 'testUser4',
                'password': 'password'}

        setup_response = self.client.post('/api/auth/register', data, format='json')

        self.assertEqual(setup_response.status_code, status.HTTP_201_CREATED, 'Register response status not correct')
        token = setup_response.data.get('token')

        # get user request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/auth/user')

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertEqual(response.data.get('username'), 'testUser4')
