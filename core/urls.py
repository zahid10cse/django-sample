from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import CoreViewSet

router = DefaultRouter()

router.register(r'', CoreViewSet, basename='core')

# Put here all apps url
urlpatterns = [
    path('', include(router.urls)),
]
