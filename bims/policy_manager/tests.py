from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import Policy
from intent_manager.models import Intent
from user_manager.models import User
from refiner.models import Currency

import pickle

from refiner.irtk.policy import Policy as irtkPolicy, CostProfile, Interval, BlockchainType, Currency as irtkCurrency, Time
from refiner.irtk.intent import Blockchain


class PolicyManagerTests(APITestCase):
    client = APIClient
    url = '/api/policies/'
    token = None

    def setUp(self) -> None:

        # obtain a valid token
        credentials = {'username': 'testUser0',
                       'password': 'password'}
        user_response = self.client.post('/api/auth/register', credentials, format='json')
        self.token = user_response.data.get('token')
        self.user_id = user_response.data.get('user').get('id')

    def test_get_policies(self):

        # save all necessary models
        user = User.objects.get()
        user.save()
        intent = Intent(username=user, intent_string='For client1 select the fastest Blockchain until the daily costs '
                                                     'reach 24')
        intent.save()
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

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.url + '?intent_id=' + str(intent.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Incorrect status code')
        self.assertEqual(response.data[0]['id'], policy.id, 'Policy IDs do not match.')
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
