from django.urls import path
from .views import MyTokenObtainPairView, RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]