from rest_framework import routers
from .api import PolicyViewSet


router = routers.DefaultRouter()
router.register('api/policies', PolicyViewSet, 'policies')

urlpatterns = router.urls
