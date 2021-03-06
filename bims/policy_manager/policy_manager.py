from django.db import models
from policy_manager.plebeus import PleBeuS
import pickle


class PolicyManager(models.Manager):
    """Manager class for Policy model"""

    def create_policy(self, raw_policy, intent_id):
        """
        Creates a Policy and stores it in the database. Takes the output of the IRTK and
        an intent_id as a foreign key to the parent intent as input.
        Also saves the policy to PleBeuS. The id of the policy in PleBeuS is also stored.
        Returns the created policy.
        """

        # save policy to PleBeuS
        pbs = PleBeuS()
        pbs_id = pbs.save_policy(raw_policy, '')

        policy = self.create(
            intent_id_id=intent_id,
            pbs_id=pbs_id,
            user=raw_policy.user,
            cost_profile=str(raw_policy.cost_profile),
            timeframe_start=str(raw_policy.timeframe_start),
            timeframe_end=str(raw_policy.timeframe_end),
            interval=str(raw_policy.interval),
            currency_id=raw_policy.currency.name,
            threshold=raw_policy.threshold,
            split_txs=raw_policy.split_txs,
            blockchain_pool=pickle.dumps(raw_policy.blockchain_pool),  # pickle the set containing the blockchain_pool
            blockchain_type=str(raw_policy.blockchain_type),
            min_tx_rate=raw_policy.min_tx_rate,
            max_block_time=raw_policy.max_block_time,
            min_data_size=raw_policy.min_data_size,
            max_tx_cost=raw_policy.max_tx_cost,
            min_popularity=raw_policy.min_popularity,
            min_stability=raw_policy.min_stability,
            turing_complete=raw_policy.turing_complete,
            encryption=raw_policy.encryption,
            redundancy=raw_policy.redundancy,
        )
        return policy
