from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()

# Put here all apps url
urlpatterns = [
    path('', include(router.urls)),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('core/', include('core.urls')),
]
