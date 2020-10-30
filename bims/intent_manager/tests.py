from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.test import override_settings
from intent_manager.models import Intent
from user_manager.models import User
from refiner.models import Currency
from policy_manager.models import Policy
import time
import pickle


@override_settings(USE_PLEBEUS=False)
class IntentManagerTests(APITestCase):
    client = APIClient
    url = '/api/intents/'
    token = None
    user_id = None

    def setUp(self) -> None:
        # obtain a valid token
        credentials = {'username': 'testUser0',
                       'password': 'password'}
        user_response = self.client.post('/api/auth/register', credentials, format='json')
        self.token = user_response.data.get('token')
        self.user_id = user_response.data.get('user').get('id')

        # save currencies to database
        usd = Currency(currency='USD', exchange_rate=1)
        chf = Currency(currency='CHF', exchange_rate=1.09)
        eur = Currency(currency='EUR', exchange_rate=1.18)
        usd.save()
        chf.save()
        eur.save()

    def test_get_intents_unauthorized(self):
        """tests GET request without a token, expects a 401 status code"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Incorrect status code')

    def test_get_intents(self):
        """tests GET request with token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')

    def test_post_intent(self):
        """test POST request of an intent"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        intent = 'For client1 select the fastest Blockchain until the daily costs reach CHF 20'
        data = {'intent_string': intent}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Incorrect status code')
        self.assertEqual(Intent.objects.count(), 1, 'Incorrect number of intents')
        self.assertEqual(Intent.objects.get().username.id, self.user_id, 'Incorrect user_id in intent')

    def test_post_invalid_intent(self):
        """test POST request of an invalid intent"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        intent = 'For client1 select the fastest Blockchain asd'
        data = {'intent_string': intent}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Incorrect status code')
        self.assertEqual(Intent.objects.count(), 0, 'Intent was created, although not valid')
        self.assertTrue(len(response.data.get('expected')) != 0, 'Expected array is empty')

    def test_update_intent(self):
        """test PUT request to update an existing intent"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # save an intent and policy to the database
        existing_intent = Intent(username=User.objects.get(), intent_string='For client1 select the fastest '
                                                                            'Blockchain until the daily costs reach 20')
        existing_intent.save()
        usd = Currency(currency='USD', exchange_rate=1)
        policy = Policy(
            user='client1',
            cost_profile='CostProfile.PERFORMANCE',
            timeframe_start='Time.DEFAULT',
            timeframe_end='Time.DEFAULT',
            interval='Interval.DAILY',
            threshold=20.0,
            split_txs=False,
            blockchain_pool=pickle.dumps([]),
            blockchain_type='BlockchainType.INDIFFERENT',
            min_tx_rate=4,
            max_block_time=600,
            min_data_size=20,
            max_tx_cost=0.0,
            min_popularity=0.0,
            min_stability=0.0,
            turing_complete=False,
            encryption=False,
            redundancy=False,
            intent_id=existing_intent,
            currency=usd,
        )
        policy.save()

        time.sleep(0.01)  # test was flaky: created_at and updated_at were sometimes equal

        # id of existing intent
        intent_id = Intent.objects.get().id

        new_intent = 'For client2 select the cheapest Blockchain until the daily costs reach EUR 30'
        data = {'intent_string': new_intent}

        response = self.client.put(self.url + str(intent_id) + '/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertEqual(Intent.objects.get().intent_string, new_intent, 'intent_string was not updated')
        self.assertNotEqual(Intent.objects.get().created_at, Intent.objects.get().updated_at,
                            'created_at and updated_at timestamp are equal')

    def test_delete_intent(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        existing_intent = Intent(username=User.objects.get(), intent_string='For client1 select the fastest '
                                                                            'Blockchain until the daily costs reach '
                                                                            'CHF 20')
        existing_intent.save()

        response = self.client.delete(self.url + str(existing_intent.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Incorrect status code')
        self.assertFalse(Intent.objects.filter(id=existing_intent.id), 'Intent was not deleted')

    def test_delete_intent_with_policies(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        existing_intent = Intent(username=User.objects.get(), intent_string='For client1 select the fastest '
                                                                            'Blockchain until the daily costs reach '
                                                                            'CHF 20')
        existing_intent.save()
        policy = Policy(intent_id=existing_intent,
                        currency=Currency.objects.get(currency='USD'))
        policy.save()

        self.assertTrue(Policy.objects.filter(intent_id=existing_intent.id), 'Policy was not created in set-up')

        response = self.client.delete(self.url + str(existing_intent.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Incorrect status code')
        self.assertFalse(Intent.objects.filter(id=existing_intent.id), 'Intent was not deleted')
        self.assertFalse(Policy.objects.filter(intent_id=existing_intent.id), 'Policy of intent was not deleted')
