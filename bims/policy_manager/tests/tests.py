from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import override_settings

from policy_manager.models import Policy
from intent_manager.models import Intent
from user_manager.models import User
from refiner.models import Currency

import pickle

from refiner.irtk.policy import Policy as irtkPolicy, CostProfile, Interval, BlockchainType, Currency as irtkCurrency, \
    Time
from refiner.irtk.intent import Blockchain


@override_settings(USE_PLEBEUS=False)
class PolicyManagerTests(APITestCase):
    client = APIClient
    url = '/api/policies/'
    token = None

    intent_id = None
    policy_id = None

    def setUp(self) -> None:
        # obtain a valid token
        credentials = {'username': 'testUser0',
                       'password': 'password'}
        user_response = self.client.post('/api/auth/register', credentials, format='json')
        self.token = user_response.data.get('token')
        self.user_id = user_response.data.get('user').get('id')

    def save_policy(self) -> None:
        """helper function to save a policy with an intent and currency to the database"""
        user = User.objects.get()
        user.save()
        intent = Intent(username=user, intent_string='For client1 select the fastest Blockchain until the daily costs '
                                                     'reach 24')
        intent.save()
        self.intent_id = intent.id
        currency = Currency(currency='USD', exchange_rate=1)
        currency.save()
        policy = Policy(
            user='client1',
            cost_profile='CostProfile.PERFORMANCE',
            timeframe_start='Time.DEFAULT',
            timeframe_end='Time.DEFAULT',
            interval='Interval.DAILY',
            threshold=24.0,
            split_txs=False,
            blockchain_pool=pickle.dumps({Blockchain.ETHEREUM, Blockchain.STELLAR}),
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
            intent_id=intent,
            currency=currency
        )
        policy.save()
        self.policy_id = policy.id

    def test_get_policies(self):
        self.save_policy()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.url + '?intent_id=' + str(self.intent_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertEqual(response.data[0]['id'], self.policy_id, 'Policy IDs do not match.')
        self.assertEqual(sorted(response.data[0]['blockchain_pool']), ['ETHEREUM', 'STELLAR'],
                         'Incorrect blockchain pool')

    def test_create_policy(self):
        # set up necessary models
        usd = Currency(currency='USD', exchange_rate=1)
        usd.save()
        user = User(username='testUser1')
        user.save()
        intent = Intent(username=user, intent_string='For client1 select the fastest Blockchain until the daily costs '
                                                     'reach 24')
        intent.save()

        blockchain_pool = {Blockchain.BITCOIN, Blockchain.STELLAR, Blockchain.ETHEREUM}
        policy_user = 'client1'

        raw_policy = irtkPolicy(
            user=policy_user,
            cost_profile=CostProfile.PERFORMANCE,
            timeframe_start=Time.DEFAULT,
            timeframe_end=Time.DEFAULT,
            interval=Interval.DAILY,
            currency=irtkCurrency.USD,
            threshold=24.0,
            split_txs=False,
            blockchain_pool=blockchain_pool,
            blockchain_type=BlockchainType.INDIFFERENT,
            min_tx_rate=4,
            max_block_time=600,
            min_data_size=20,
            max_tx_cost=0.0,
            min_popularity=0.0,
            min_stability=0.0,
            turing_complete=False,
            encryption=False,
            redundancy=False
        )

        Policy.objects.create_policy(raw_policy, intent.id)

        policy = Policy.objects.filter(intent_id=intent.id).get()
        self.assertEqual(len(Policy.objects.filter(intent_id=intent.id)), 1, 'Number of Policies with corresponding '
                                                                             'intent_id was incorrect')
        self.assertEqual(policy.user, policy_user, 'User in policy is incorrect')
        self.assertEqual(policy.threshold, 24, 'Threshold was incorrect')
        self.assertEqual(pickle.loads(policy.blockchain_pool), blockchain_pool, 'Blockchain Pool is incorrect')

    def test_is_policy_deleted(self):
        self.save_policy()

        self.assertNotEqual(len(Policy.objects.all()), 0, 'Policy creation in set up failed')

        intent = Intent.objects.get()
        intent.delete()

        self.assertEqual(len(Policy.objects.all()), 0, 'Policy was not deleted')

    def test_unauthorized_get_request(self):
        self.save_policy()

        response = self.client.get(self.url + '?intent_id=' + str(self.intent_id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Incorrect status code')
        self.assertEqual(response.data.get('detail').code, 'not_authenticated')

    def test_post_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'incorrect status code; '
                                                                                   'post method is allowed')
        self.assertEqual(response.data.get('detail').code, 'method_not_allowed')

    def test_put_request(self):
        self.save_policy()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(self.url + str(self.policy_id) + '/', {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'incorrect status code; '
                                                                                   'put method is allowed')
        self.assertEqual(response.data.get('detail').code, 'method_not_allowed')

    def test_delete_request(self):
        self.save_policy()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(self.url + str(self.policy_id) + '/')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'incorrect status code; '
                                                                                   'delete method is allowed')
        self.assertEqual(response.data.get('detail').code, 'method_not_allowed')
