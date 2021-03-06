from django.conf import settings
import requests
import json
from .plebeusException import PlebeusException
from requests.exceptions import ConnectionError


class PleBeuS:

    pbs_url = settings.PLEBEUS_URL
    headers = {'Content-Type': 'application/json'}

    @staticmethod
    def __map_blockchain_pool(policy) -> list:
        blockchains = {'bitcoin': 'BTC',
                       'ethereum': 'ETH',
                       'eos': 'EOS',
                       'iota': 'MIOTA',
                       'hyperledger': 'HYP',
                       'multichain': 'MLC',
                       'stellar': 'XLM',
                       }
        preferredBC = []
        for bc in policy.blockchain_pool:
            preferredBC.append(blockchains[bc.value])
        return preferredBC

    def __construct_policy_data(self, policy, pbs_id: str):
        """Maps a Policy to a JSON object for requests to PleBeuS."""
        if type(policy.blockchain_type) == str:
            bcType = policy.blockchain_type
        else:
            bcType = policy.blockchain_type.value
        return json.dumps({
            'preferredBC': self.__map_blockchain_pool(policy),
            'currency': policy.currency.name,
            'bcTuringComplete': str(policy.turing_complete).lower(),
            'split': str(policy.split_txs).lower(),
            'timeFrameStart': policy.timeframe_start.value,
            'timeFrameEnd': policy.timeframe_end.value,
            'costProfile': policy.cost_profile.value,
            '_id': pbs_id,
            'username': policy.user,
            'cost': policy.threshold,
            'bcType': bcType,
            'interval': policy.interval.value,
            'bcTps': policy.min_tx_rate,
            'bcBlockTime': policy.max_block_time,
            'bcDataSize': policy.min_data_size,
        })

    @staticmethod
    def __construct_default_policy_data(user: str):
        return json.dumps({
            'preferredBC': [],
            'currency': 'USD',
            'bcTuringComplete': "false",
            'split': "false",
            'timeFrameStart': '00:00',
            'timeFrameEnd': '00:00',
            'costProfile': 'performance',
            '_id': '',
            'username': user,
            'cost': 0.0,
            'bcType': 'indifferent',
            'interval': 'default',
            'bcTps': 4,
            'bcBlockTime': 600,
            'bcDataSize': 20,
        })

    @staticmethod
    def __is_default_policy(policy) -> bool:
        """Helper function, returns boolean if policy is a default policy or not"""
        return policy.interval.value == 'default'

    def save_policy(self, policy, pbs_id: str) -> str:
        """Makes a POST request to PleBeuS. Either creates a new Policy or updates an existing one if a pbs_id is
        provided. Returns the pbs_id"""
        if not settings.USE_PLEBEUS:
            return ''
        try:
            get_user_response = requests.get(self.pbs_url + '/policies/' + policy.user)
            if get_user_response.status_code == 404 and not self.__is_default_policy(policy):
                # need to create a default policy first
                default_policy_response = requests.post(self.pbs_url + '/api/policies',
                                                        self.__construct_default_policy_data(policy.user),
                                                        headers=self.headers)
                if default_policy_response.status_code != 201:
                    # error when creating default policy
                    raise PlebeusException(json.loads(default_policy_response.text).get('message'))
            data = self.__construct_policy_data(policy, pbs_id)
            response = requests.post(self.pbs_url + '/api/policies', data, headers=self.headers)
            if response.status_code != 201:
                raise PlebeusException(json.loads(response.text).get('message'))
            return json.loads(response.text).get('policy').get('_id')
        except ConnectionError:
            raise PlebeusException('Connection to PleBeuS failed')

    def delete_policy(self, pbs_id: str) -> None:
        """Makes a DELETE request to PleBeuS."""
        if not settings.USE_PLEBEUS:
            return
        try:
            requests.delete(self.pbs_url + '/api/policy/' + pbs_id)
        except ConnectionError:
            raise PlebeusException('Connection to PleBeuS failed')
