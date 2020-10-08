from rest_framework import generics, permissions, status
from .serializers import ParserSerializer
from rest_framework.response import Response
from .refiner import refine_intent
from refiner.irtk.parser.state import IllegalTransitionError
from refiner.irtk.incompleteIntentException import IncompleteIntentException
from refiner.irtk.validation import ValidationError
from .models import Currency


class IntentParserAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ParserSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            refine_intent(request.data.get('intent_string'))
        except IllegalTransitionError as error:
            return Response({
                'message': error.message,
                'expected': error.expected
            }, status=status.HTTP_200_OK)
        except IncompleteIntentException as error:
            return Response({
                'message': error.message,
                'expected': error.expected
            }, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response({
                'message': error.message,
                'expected': error.expected
            }, status=status.HTTP_200_OK)
        except Currency.DoesNotExist:
            return Response({
                'message': 'Currency was not found',
                'expected': []
            }, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
