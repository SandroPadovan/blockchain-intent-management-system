from django.urls import path
from .api import IntentParserAPI


urlpatterns = [
    path('api/parser', IntentParserAPI.as_view()),
]
