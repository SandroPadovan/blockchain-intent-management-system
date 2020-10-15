from rest_framework import generics, permissions, status
from .serializers import ParserSerializer
from rest_framework.response import Response
from .refiner import refine_intent
from refiner.irtk.parser.state import IllegalTransitionError
from refiner.irtk.incompleteIntentException import IncompleteIntentException
from refiner.irtk.validation import ValidationError
from .models import Currency


class IntentParserAPI(generics.GenericAPIView):
    """Implements the Parser API to parse an Intent for text suggestions."""
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ParserSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        """Handles POST requests. If intent is not valid, returns status 200 with expected words.
        If Intent is valid, returns status 204.
        """
        try:
            refine_intent(request.data.get('intent_string'))
        except (IllegalTransitionError, IncompleteIntentException, ValidationError) as error:
            # Intent is not valid
            return Response({
                'message': error.message,
                'expected': error.expected
            }, status=status.HTTP_200_OK)
        except Currency.DoesNotExist:
            return Response({
                'message': 'Currency was not found',
                'expected': []
            }, status=status.HTTP_404_NOT_FOUND)

        # Intent is valid
        return Response(status=status.HTTP_204_NO_CONTENT)
