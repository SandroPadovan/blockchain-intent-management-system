from intent_manager.models import Intent
from .serializers import IntentSerializer
from refiner.refiner import refine_intent, save_policies, update_policies
from refiner.irtk.parser.state import IllegalTransitionError
from refiner.irtk.incompleteIntentException import IncompleteIntentException
from refiner.irtk.validation import ValidationError

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied


class IntentViewSet(viewsets.ModelViewSet):
    """ViewSets offer CRUD functionality without having to specify explicit methods for creating, retrieving etc."""
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = IntentSerializer

    def get_queryset(self):
        """returns a queryset containing all intents"""
        return self.request.user.intents.all()

    def create(self, request, *args, **kwargs):
        """Passes the intent to the refiner. Saves the intent if valid and saves the policies"""
        try:
            policies = refine_intent(request.data.get('intent_string'))
        except IllegalTransitionError as error:
            return Response({
                'message': error.message,
                'expected': error.expected
            }, status=status.HTTP_400_BAD_REQUEST)
        except IncompleteIntentException as error:
            return Response({
                'message': error.message,
                'expected': error.expected
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as error:
            return Response({
                'message': error.message,
                'expected': error.expected
            }, status=status.HTTP_400_BAD_REQUEST)

        intent = Intent(username=request.user,
                        intent_string=request.data.get('intent_string'))
        intent.save()
        save_policies(policies, intent.id)

        return Response({
            'id': intent.id,
            'created_at': intent.created_at,
            'updated_at': intent.updated_at,
            'intent_string': intent.intent_string,
            'username': intent.username.id
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """updates an intent"""
        intent = Intent.objects.get(id=kwargs.get('pk'))

        # if intent user and request user don't match
        if request.user != intent.username:
            raise PermissionDenied

        policies = refine_intent(request.data.get('intent_string'))
        intent.intent_string = request.data.get('intent_string')
        intent.save()

        update_policies(policies, intent.id)

        return Response({
            'id': intent.id,
            'created_at': intent.created_at,
            'updated_at': intent.updated_at,
            'intent_string': intent.intent_string,
            'username': intent.username.id
        }, status=status.HTTP_200_OK)
