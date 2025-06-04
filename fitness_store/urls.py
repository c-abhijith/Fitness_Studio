# fitness_store/urls.py

from django.urls import path
from .views import MyScheduleView

urlpatterns = [
    path('workingtime/', TranerScheduleView.as_view(), name='my_schedule'),
]
