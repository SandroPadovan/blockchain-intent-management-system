from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class ParserTests(APITestCase):
    client = APIClient
    url = '/api/parser'
    token = None

    def setUp(self) -> None:
        # obtain a valid token
        credentials = {'username': 'testUser0',
                       'password': 'password'}
        user_response = self.client.post('/api/auth/register', credentials, format='json')
        self.token = user_response.data.get('token')
        self.user_id = user_response.data.get('user').get('id')

    def test_empty_string(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.post(self.url, {'intent_string': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertEqual(response.data.get('expected'), {'for'}, 'Expected words not as expected')

    def test_valid_intent(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        intent = 'for client1 select the fastest blockchain as default'

        response = self.client.post(self.url, {'intent_string': intent}, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Incorrect status code')

    def test_incomplete_intent(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        intent = 'for client1 select the'

        response = self.client.post(self.url, {'intent_string': intent}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertEqual(response.data.get('message'), 'Intent is incomplete', 'Unexpected message in response')
        self.assertEqual(response.data.get('expected'), {'fastest', 'cheapest'}, 'Expected words not as expected')

    def test_incorrect_intent(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        intent = 'for client1 select the cheapest sdofiae asdoifjae adiofeifaoehj'

        response = self.client.post(self.url, {'intent_string': intent}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertNotEqual(response.data.get('message'), 'Intent is incomplete', 'Unexpected message in response')
        self.assertEqual(response.data.get('expected'),
                         {'blockchain', 'public', 'private', 'fast', 'cheap', 'popular', 'stable'},
                         'Expected words not as expected')
