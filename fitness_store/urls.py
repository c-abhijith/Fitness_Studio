from django.urls import path
from views.fitness_views import FitnessClassListCreateView
from views.booking_views import BookingListCreateView,BookingDetailView

urlpatterns = [
    path('classes/', FitnessClassListCreateView.as_view(), name='fitness-class-list-create'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<uuid:id>/', BookingDetailView.as_view(), name='booking-detail'),

]
