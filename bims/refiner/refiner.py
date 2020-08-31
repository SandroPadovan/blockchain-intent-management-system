from typing import List, Optional

from .irtk import refine
from policy_manager.models import Policy
from refiner.irtk.refiner import Policy as irtkPolicy
import pickle


def refine_intent(intent: str) -> Optional[List[irtkPolicy]]:
    """refines an intent and returns a list of resulting policies"""
    policies = refine(intent)
    return policies


def save_policies(policies: list, intent_id: int) -> None:
    """takes a list of policies and an intent_id as input, creates and saves the policies with the intent_id"""
    for policy in policies:
        Policy.objects.create_policy(policy, intent_id)


def update_policies(new_policies: List[irtkPolicy], intent_id: int) -> None:
    """Updates existing policies. In case the number of policies corresponding to an intent changes,
    policies are added or deleted."""
    old_policies = Policy.objects.filter(intent_id=intent_id)   # get policies with the corresponding intent_id
    num_old_policies = len(old_policies)
    num_new_policies = len(new_policies)

    if num_old_policies <= num_new_policies:     # possibly need to create additional policies

        # update existing policies
        for i in range(len(old_policies)):
            updated = overwrite_policy_fields(old_policies[i], new_policies[i], intent_id)
            updated.save()

        # possibly create new policies
        j = num_new_policies - num_old_policies     # number of new policies to be created
        for i in range(j):
            Policy.objects.create_policy(new_policies[num_old_policies + i], intent_id)

    else:   # need to delete policies

        # delete unnecessary policies
        j = num_old_policies - num_new_policies     # number of old policies to be deleted
        for i in range(j):
            p = Policy.objects.filter(intent_id=intent_id).first()
            p.delete()

        # update remaining policies
        remaining_policies = Policy.objects.filter(intent_id=intent_id)
        i = 0
        for policy in new_policies:
            updated = overwrite_policy_fields(remaining_policies[i], policy, intent_id)
            updated.save()
            i += 1


def overwrite_policy_fields(policy: Policy, raw_policy: irtkPolicy, intent_id: int) -> Policy:
    """takes a Policy object and overwrites/updates its fields with values from a irtkPolicy (raw_policy)"""
    policy.intent_id_id = intent_id
    policy.user = raw_policy.user
    policy.cost_profile = raw_policy.cost_profile
    policy.timeframe_start = raw_policy.timeframe_start
    policy.timeframe_end = raw_policy.timeframe_end
    policy.interval = raw_policy.interval
    policy.currency_id = raw_policy.currency.name
    policy.threshold = raw_policy.threshold
    policy.split_txs = raw_policy.split_txs
    policy.blockchain_pool = pickle.dumps(raw_policy.blockchain_pool)
    policy.blockchain_type = raw_policy.blockchain_type
    policy.min_tx_rate = raw_policy.min_tx_rate
    policy.max_block_time = raw_policy.max_block_time
    policy.min_data_size = raw_policy.min_data_size
    policy.max_tx_cost = raw_policy.max_tx_cost
    policy.min_popularity = raw_policy.min_popularity
    policy.min_stability = raw_policy.min_stability
    policy.turing_complete = raw_policy.turing_complete
    policy.encryption = raw_policy.encryption
    policy.redundancy = raw_policy.redundancy
    return policy
