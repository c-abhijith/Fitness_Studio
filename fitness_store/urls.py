# fitness_store/urls.py

from django.urls import path
from .views import WorkingHourList

urlpatterns = [
    path('workingtime/', WorkingHourList.as_view(), name='working_hour'),
]
