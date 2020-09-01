from .models import Policy
from intent_manager.models import Intent
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import PolicySerializer
from django.core.exceptions import PermissionDenied
import pickle


class PolicyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Policy API. Read only, since Policies are only created by the refiner, not via the API."""
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PolicySerializer

    @staticmethod
    def is_intent_owner(user, intent_id):
        """Checks if a user is the owner of an intent"""
        intent = Intent.objects.get(id=intent_id)
        return intent.username == user

    def get_queryset(self):
        """returns a queryset of policies corresponding to an intent specified in the query parameters,
        if the user is the owner of the intent"""
        intent_id = self.request.query_params.get('intent_id', None)
        if self.is_intent_owner(self.request.user, intent_id):
            queryset = Policy.objects.filter(intent_id_id=intent_id)
            return queryset
        raise PermissionDenied

    def list(self, request, *args, **kwargs):
        """Handles the GET request for policies. Unpickles the blockchain_pool of each policy"""
        queryset = self.get_queryset().values()
        for policy in queryset:
            policy['blockchain_pool'] = pickle.loads(policy['blockchain_pool'])
            blockchain_pool = []
            for blockchain in policy['blockchain_pool']:
                blockchain_pool.append(blockchain.name)
            policy['blockchain_pool'] = blockchain_pool
        return Response(queryset, content_type='application/json')
