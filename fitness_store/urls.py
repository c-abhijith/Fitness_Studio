from django.urls import path
from .views import FitnessClassListCreateView, FitnessClassDetailView

urlpatterns = [
    path('classes/', FitnessClassListCreateView.as_view(), name='fitness-class-list-create'),
    path('classes/<uuid:pk>/', FitnessClassDetailView.as_view(), name='fitness-class-detail'),
]
