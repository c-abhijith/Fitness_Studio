# fitness_store/serializers.py

from rest_framework import serializers
from .models import Trainer

class TrainerScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['weekly_schedule']
