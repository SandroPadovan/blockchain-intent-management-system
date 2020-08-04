from .irtk import refine
from policy_manager.models import Policy


def refine_intent(intent):
    """refines an intent and returns a list of resulting policies"""
    policies = refine(intent.validated_data.get('intent_string'))
    return policies


def save_policies(policies, intent_id):
    """takes a list of policies and an intent_id as input, saves the policies with the intent_id"""
    for policy in policies:
        Policy.objects.create_policy(policy, intent_id)
