from intent_manager.models import Intent
from rest_framework import viewsets, permissions
from .serializers import IntentSerializer
from refiner.refiner import refine_intent, save_policies


class IntentViewSet(viewsets.ModelViewSet):
    """ViewSets offer CRUD functionality without having to specify explicit methods for creating, retrieving etc."""
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = IntentSerializer

    def get_queryset(self):
        """returns a queryset containing all intents"""
        return Intent.objects.all()

    def perform_create(self, serializer):
        """Passes the intent to the refiner. Saves the intent if valid and saves the policies"""
        policies = refine_intent(serializer)
        intent_id = serializer.save().id
        save_policies(policies, intent_id)
