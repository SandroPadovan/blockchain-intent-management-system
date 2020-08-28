from .irtk import refine
from policy_manager.models import Policy


def refine_intent(intent: str):
    """refines an intent and returns a list of resulting policies"""
    policies = refine(intent)
    return policies


def save_policies(policies, intent_id) -> None:
    """takes a list of policies and an intent_id as input, creates and saves the policies with the intent_id"""
    for policy in policies:
        Policy.objects.create_policy(policy, intent_id)


def update_policies(policies, intent_id) -> None:
    """Updates existing policies by deleting the existing policies corresponding to an intent and saving the new
    policies of the updated intent. """
    # delete existing policies of given intent
    old_policies = Policy.objects.filter(intent_id=intent_id)
    for policy in old_policies:
        policy.delete()

    # create new policies
    save_policies(policies, intent_id)
