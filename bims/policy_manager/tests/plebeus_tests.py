from unittest.mock import PropertyMock, patch
from django.test import TestCase, override_settings
from django.conf import settings
import json

from policy_manager.plebeus import PleBeuS
from policy_manager.plebeusException import PlebeusException
from refiner.irtk.policy import Policy as irtkPolicy, CostProfile, Interval, BlockchainType, Currency as irtkCurrency, \
    Time
from refiner.irtk.intent import Blockchain


class PlebeusTests(TestCase):
    pbs = PleBeuS()

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
    mock_response_data = json.dumps({
        'message': 'This is a message from the mock request.',
        'policy': {'_id': '829919'}
    })

    @patch('policy_manager.plebeus.requests.get')
    @patch('policy_manager.plebeus.requests.post')
    def test_create_policy_with_existing_user(self, mock_post, mock_get):
        type(mock_get.return_value).status_code = PropertyMock(return_value=200)
        type(mock_post.return_value).status_code = PropertyMock(return_value=201)
        type(mock_post.return_value).text = PropertyMock(return_value=self.mock_response_data)

        res = self.pbs.save_policy(self.policy, '')

        self.assertNotEqual(res, '', 'No pbs_id was returned from save_policy()')
        mock_post.assert_called_once_with(settings.PLEBEUS_URL + '/api/policies',
                                          '{"preferredBC": ["BTC"], '
                                          '"currency": "USD", '
                                          '"bcTuringComplete": "false", '
                                          '"split": "false", '
                                          '"timeFrameStart": "00:00", '
                                          '"timeFrameEnd": "00:00", '
                                          '"costProfile": "performance", '
                                          '"_id": "", '
                                          '"username": "client1", '
                                          '"cost": 24.0, '
                                          '"bcType": "indifferent", '
                                          '"interval": "daily", '
                                          '"bcTps": 4, '
                                          '"bcBlockTime": 600, '
                                          '"bcDataSize": 20}',
                                          headers={'Content-Type': 'application/json'})

    @patch('policy_manager.plebeus.requests.get')
    @patch('policy_manager.plebeus.requests.post')
    def test_save_policy_with_new_user(self, mock_post, mock_get):
        type(mock_get.return_value).status_code = PropertyMock(return_value=404)
        type(mock_post.return_value).status_code = PropertyMock(return_value=201)
        type(mock_post.return_value).text = PropertyMock(return_value=self.mock_response_data)

        res = self.pbs.save_policy(self.policy, '')

        self.assertNotEqual(res, '', 'No pbs_id was returned from save_policy()')
        mock_post.assert_called()
        mock_post.assert_any_call(settings.PLEBEUS_URL + '/api/policies',
                                  '{"preferredBC": ["BTC"], '
                                  '"currency": "USD", '
                                  '"bcTuringComplete": "false", '
                                  '"split": "false", '
                                  '"timeFrameStart": "00:00", '
                                  '"timeFrameEnd": "00:00", '
                                  '"costProfile": "performance", '
                                  '"_id": "", '
                                  '"username": "client1", '
                                  '"cost": 24.0, '
                                  '"bcType": "indifferent", '
                                  '"interval": "daily", '
                                  '"bcTps": 4, '
                                  '"bcBlockTime": 600, '
                                  '"bcDataSize": 20}',
                                  headers={'Content-Type': 'application/json'})
        mock_post.assert_any_call(settings.PLEBEUS_URL + '/api/policies',
                                  '{"preferredBC": [], '
                                  '"currency": "USD", '
                                  '"bcTuringComplete": "false", '
                                  '"split": "false", '
                                  '"timeFrameStart": "00:00", '
                                  '"timeFrameEnd": "00:00", '
                                  '"costProfile": "performance", '
                                  '"_id": "", '
                                  '"username": "client1", '
                                  '"cost": 0.0, '
                                  '"bcType": "indifferent", '
                                  '"interval": "default", '
                                  '"bcTps": 4, '
                                  '"bcBlockTime": 600, '
                                  '"bcDataSize": 20}',
                                  headers={'Content-Type': 'application/json'})

    @patch('policy_manager.plebeus.requests.get')
    @patch('policy_manager.plebeus.requests.post')
    def test_update_existing_policy(self, mock_post, mock_get):
        type(mock_get.return_value).status_code = PropertyMock(return_value=200)
        type(mock_post.return_value).status_code = PropertyMock(return_value=201)
        type(mock_post.return_value).text = PropertyMock(return_value=self.mock_response_data)

        pbs_id = '123456789'

        res = self.pbs.save_policy(self.policy, pbs_id)

        self.assertNotEqual(res, '')
        mock_post.assert_called_once_with(settings.PLEBEUS_URL + '/api/policies',
                                          '{"preferredBC": ["BTC"], '
                                          '"currency": "USD", '
                                          '"bcTuringComplete": "false", '
                                          '"split": "false", '
                                          '"timeFrameStart": "00:00", '
                                          '"timeFrameEnd": "00:00", '
                                          '"costProfile": "performance", '
                                          '"_id": "' + pbs_id + '", '
                                          '"username": "client1", '
                                          '"cost": 24.0, '
                                          '"bcType": "indifferent", '
                                          '"interval": "daily", '
                                          '"bcTps": 4, '
                                          '"bcBlockTime": 600, '
                                          '"bcDataSize": 20}',
                                          headers={'Content-Type': 'application/json'})

    @patch('policy_manager.plebeus.requests.get')
    @patch('policy_manager.plebeus.requests.post')
    def test_save_policy_failed(self, mock_post, mock_get):
        type(mock_get.return_value).status_code = PropertyMock(return_value=200)
        type(mock_post.return_value).status_code = PropertyMock(return_value=500)
        type(mock_post.return_value).text = PropertyMock(return_value=self.mock_response_data)

        self.assertRaisesMessage(PlebeusException,
                                 'This is a message from the mock request',
                                 self.pbs.save_policy, self.policy, '')
        mock_post.assert_called_once()

    @override_settings(USE_PLEBEUS=False)
    @patch('policy_manager.plebeus.requests.get')
    @patch('policy_manager.plebeus.requests.post')
    def test_save_policy_without_plebeus(self, mock_post, mock_get):
        res = self.pbs.save_policy(self.policy, '')

        self.assertEqual(res, '')
        mock_get.assert_not_called()
        mock_post.assert_not_called()

    @override_settings(USE_PLEBEUS=False)
    @patch('policy_manager.plebeus.requests.delete')
    def test_delete_policy_without_plebeus(self, mock_delete):
        self.pbs.delete_policy('8238129')

        mock_delete.assert_not_called()

    @patch('policy_manager.plebeus.requests.delete')
    def test_delete_policy(self, mock_delete):
        pbs_id = '123456789'

        self.pbs.delete_policy(pbs_id)

        mock_delete.assert_called_once_with(settings.PLEBEUS_URL + '/api/policy/' + pbs_id)
