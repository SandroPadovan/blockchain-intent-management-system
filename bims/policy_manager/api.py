from .models import Policy
from intent_manager.models import Intent
from rest_framework import viewsets, permissions
from .serializers import PolicySerializer
from django.core.exceptions import PermissionDenied


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
        """returns policies corresponding to an intent specified in the query parameters,
        if the user is the owner of the intent"""
        intent_id = self.request.query_params.get('intent_id', None)
        if self.is_intent_owner(self.request.user, intent_id):
            queryset = Policy.objects.filter(intent_id_id=intent_id)
            return queryset

        raise PermissionDenied
