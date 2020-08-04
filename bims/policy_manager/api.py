from .models import Policy
from rest_framework import viewsets, permissions
from .serializers import PolicySerializer


class PolicyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Policy API. Read only, since Policies are only created by the refiner, not via the API."""
    queryset = Policy.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PolicySerializer
