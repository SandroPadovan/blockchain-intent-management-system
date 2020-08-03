from intent_manager.models import Intent
from rest_framework import viewsets, permissions
from .serializers import IntentSerializer


class IntentViewSet(viewsets.ModelViewSet):
    """ViewSets offer CRUD functionality without having to specify explicit methods for creating, retrieving etc."""
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = IntentSerializer
    queryset = Intent.objects.all()
