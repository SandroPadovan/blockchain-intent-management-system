import requests
import json
from .plebeusException import PlebeusException
from requests.exceptions import ConnectionError


class PleBeuS:

    # TODO: config file?
    pbs_url = 'http://130.60.156.183:3000'
    headers = {'Content-Type': 'application/json'}

    @staticmethod
    def map_blockchain_pool(policy) -> list:
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
        print(preferredBC)
        return preferredBC

    def construct_policy_data(self, policy, pbs_id: str):
        """Maps a Policy to a JSON object for requests to PleBeuS."""
        return json.dumps({
            'preferredBC': self.map_blockchain_pool(policy),
            'currency': policy.currency.name,
            'bcTuringComplete': policy.turing_complete,
            'split': policy.split_txs,
            'timeFrameStart': policy.timeframe_start.value,
            'timeFrameEnd': policy.timeframe_end.value,
            'costProfile': policy.cost_profile.value,
            '_id': pbs_id,
            'username': policy.user,
            'cost': policy.threshold,
            'bcType': policy.blockchain_type.value,
            'interval': policy.interval.value,
            'bcTps': policy.min_tx_rate,
            'bcBlockTime': policy.max_block_time,
            'bcDataSize': policy.min_data_size,
        })

    @staticmethod
    def construct_default_policy_data(user: str):
        return json.dumps({
            'preferredBC': [],
            'currency': 'USD',
            'bcTuringComplete': False,
            'split': False,
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
    def is_default_policy(policy) -> bool:
        """Helper function, returns boolean if policy is a default policy or not"""
        return policy.interval.value == 'default'

    def save_policy(self, policy, pbs_id: str):
        """Makes a POST request to PleBeuS. Either creates a new Policy or updates an existing one if a pbs_id is
        provided. """
        try:
            get_user_response = requests.get(self.pbs_url + '/policies/' + policy.user)

            if get_user_response.status_code == 404 and not self.is_default_policy(policy):
                # need to create a default policy first
                default_policy_response = requests.post(self.pbs_url + '/api/policies',
                                                        self.construct_default_policy_data(policy.user),
                                                        headers=self.headers)
                if default_policy_response.status_code != 201:
                    # error when creating default policy
                    raise PlebeusException(json.loads(default_policy_response.text).get('message'))

            if get_user_response.status_code == 200 and self.is_default_policy(policy):
                raise PlebeusException('Default Policy for this user already exists')

            data = self.construct_policy_data(policy, pbs_id)

            response = requests.post(self.pbs_url + '/api/policies', data, headers=self.headers)
            if response.status_code != 201:
                raise PlebeusException(json.loads(response.text).get('message'))
        except ConnectionError:
            raise PlebeusException('Connection to PleBeuS failed')

    def delete_policy(self, pbs_id: str) -> None:
        """Makes a DELETE request to PleBeuS."""
        try:
            # make request
            response = requests.delete(self.pbs_url + '/api/policy/' + pbs_id)
            if response.status_code != 200:
                raise PlebeusException(json.loads(response.text).get('message'))
        except ConnectionError:
            raise PlebeusException('Connection to PleBeuS failed')
