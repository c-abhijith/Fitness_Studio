from rest_framework import serializers
from .models import FitnessClass, Booking, CustomUser
from django.utils.timezone import now


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        exclude = ["deleted_at", "updated_at"]

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive minutes.")
        return value

    def validate_instructor(self, value):
        if value.role != CustomUser.Roles.INSTRUCTOR:
            raise serializers.ValidationError("Instructor must have the INSTRUCTOR role.")
        return value

    def validate_date(self, value):
        if value < now().date():
            raise serializers.ValidationError("Date cannot be in the past.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer() 
    class Meta:
        model = Booking
        fields = ['id', 'user_id', 'fitness_class']

class BookingSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user_id', 'fitness_class']

