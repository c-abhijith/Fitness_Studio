from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass,Booking
from .serializers import FitnessClassSerializer,BookingSerializer
from django.shortcuts import get_object_or_404
import pytz
from datetime import datetime, timedelta
from uuid import UUID
from rest_framework.permissions import IsAuthenticated


class FitnessClassListCreateView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            user_timezone = request.query_params.get('timezone', None)

            if not user_timezone:
                user_timezone = getattr(request.user, 'timezone', 'UTC')

            if user_timezone not in pytz.all_timezones:
                return Response(
                    {"error": "Invalid timezone provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            classes = FitnessClass.objects.all()
            result = []

            for cls in classes:
                original_dt = datetime.datetime.combine(cls.date, cls.time)
                instructor_tz = pytz.timezone(cls.instructor.timezone)
                localized_dt = instructor_tz.localize(original_dt)
                target_tz = pytz.timezone(user_timezone)
                converted_dt = localized_dt.astimezone(target_tz)
                serialized = FitnessClassSerializer(cls).data
                serialized['local_datetime'] = converted_dt.isoformat()
                result.append(serialized)

            return Response({
                "message": "Fitness classes fetched successfully.",
                "data": result
            })

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred while fetching classes: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    def post(self, request):
        try:
            data = request.data.copy()
            instructor = request.user
            data['instructor'] = str(instructor.id)

            class_date = data.get('date')
            class_time = data.get('time')
            duration = int(data.get('duration'))

            start_datetime = datetime.strptime(f"{class_date} {class_time}", "%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + timedelta(minutes=duration)

            existing_classes = FitnessClass.objects.filter(
                instructor=instructor,
                date=class_date
            )

            for cls in existing_classes:
                existing_start = datetime.combine(cls.date, cls.time)
                existing_end = existing_start + timedelta(minutes=cls.duration)

                if (start_datetime < existing_end and end_datetime > existing_start):
                    return Response({
                        "message": (
                            f"You already have a class '{cls.name}' from "
                            f"{existing_start.strftime('%I:%M %p')} to {existing_end.strftime('%I:%M %p')}. "
                            f"You can create a new class only after {existing_end.strftime('%I:%M %p')}."
                        )
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Proceed if no conflict
            serializer = FitnessClassSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Fitness class created successfully.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "message": "Validation failed.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": "Failed to create class.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            bookings = Booking.objects.filter(user_id=request.user)
            serializer = BookingSerializer(bookings, many=True)
            return Response({
                "message": "Bookings fetched successfully.",
                "data": serializer.data
            })
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch bookings: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            user = request.user
            class_id = request.data.get('fitness_class')

            try:
                new_class = FitnessClass.objects.get(id=class_id)
            except FitnessClass.DoesNotExist:
                return Response({"error": "Fitness class not found."}, status=status.HTTP_404_NOT_FOUND)

            new_start = datetime.combine(new_class.date, new_class.time)
            new_end = new_start + timedelta(minutes=new_class.duration)

            existing_bookings = Booking.objects.filter(user_id=user).select_related('fitness_class')

            for booking in existing_bookings:
                existing_class = booking.fitness_class
                exist_start = datetime.combine(existing_class.date, existing_class.time)
                exist_end = exist_start + timedelta(minutes=existing_class.duration)

                # Overlap logic
                if (new_start < exist_end and new_end > exist_start):
                    return Response({
                        "message": (
                            f"You already have a booking from "
                            f"{exist_start.strftime('%I:%M %p')} to {exist_end.strftime('%I:%M %p')}. "
                            "You cannot book another class during this time."
                        )
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=user)
                return Response({
                    "message": "Booking created successfully.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": f"Failed to create booking: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, booking_id, user):
        """
        Helper to get a booking belonging to the user, or return 404
        """
        return get_object_or_404(Booking, id=booking_id, user_id=user)

    def get(self, request, id):
        try:
            booking = self.get_object(id, request.user)
            serializer = BookingSerializer(booking)
            return Response({
                "message": "Booking retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve booking: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            booking = self.get_object(id, request.user)
            booking.delete()
            return Response({
                "message": "Booking deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "error": f"Failed to delete booking: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)