from django.urls import path
from .views import FitnessClassListCreateView,BookingListCreateView,BookingDetailView

urlpatterns = [
    path('classes/', FitnessClassListCreateView.as_view(), name='fitness-class-list-create'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<uuid:id>/', BookingDetailView.as_view(), name='booking-detail'),

]
