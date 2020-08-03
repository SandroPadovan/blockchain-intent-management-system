from rest_framework import routers
from .api import IntentViewSet


router = routers.DefaultRouter()
router.register('api/intents', IntentViewSet, 'intents')

urlpatterns = router.urls
