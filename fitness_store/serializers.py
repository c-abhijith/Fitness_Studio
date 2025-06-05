# fitness_store/serializers.py

from rest_framework import serializers
from .models import WorkingHour

class WorkingHoureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = ['weekly_schedule']
