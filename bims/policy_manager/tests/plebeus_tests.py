from unittest.mock import PropertyMock, patch
from django.test import TestCase
import json

from policy_manager.plebeus import PleBeuS
from refiner.irtk.policy import Policy as irtkPolicy, CostProfile, Interval, BlockchainType, Currency as irtkCurrency, Time
from refiner.irtk.intent import Blockchain


class PlebeusTests(TestCase):

    @patch('policy_manager.plebeus.requests.get')
    @patch('policy_manager.plebeus.requests.post')
    def test_save_policy(self, mock_post, mock_get):
        type(mock_get.return_value).status_code = PropertyMock(return_value=200)
        type(mock_post.return_value).status_code = PropertyMock(return_value=201)
        mock_response_data = json.dumps({
            'message': 'This is a message from the mock request.',
            'policy': {'_id': '829919'}
        })
        type(mock_post.return_value).text = PropertyMock(return_value=mock_response_data)

        policy = irtkPolicy(
            user='client1',
            cost_profile=CostProfile.PERFORMANCE,
            timeframe_start=Time.DEFAULT,
            timeframe_end=Time.DEFAULT,
            interval=Interval.DAILY,
            currency=irtkCurrency.USD,
            threshold=24.0,
            split_txs=False,
            blockchain_pool={Blockchain.BITCOIN},
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

        pbs = PleBeuS()
        res = pbs.save_policy(policy, '')

        self.assertNotEqual(res, '')
        self.assertTrue(mock_post.called)
