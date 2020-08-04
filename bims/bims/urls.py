from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('intent_manager.urls')),
    path('', include('policy_manager.urls')),
]
