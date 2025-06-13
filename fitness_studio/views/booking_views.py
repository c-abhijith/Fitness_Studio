from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fitness_studio.models import Booking, FitnessClass
from fitness_studio.serializers import BookingSerializer,BookingSerializerCreate
from user.models import CustomUser
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import datetime, timedelta
from common.helper.error_message import *
from common.helper.success_message import *
from common.helper.pagination import pagination
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
import pytz
from common.helper.utils import convert_timezone

class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            print("///")
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 20))

            user = request.user
            user_timezone = request.GET.get('timezone') or getattr(user, 'timezone', 'UTC')

            if user_timezone not in pytz.all_timezones:
                return handle_Bad_request("Invalid timezone provided.")
            if user.role == CustomUser.Roles.INSTRUCTOR:
                bookings = Booking.objects.filter(
                    fitness_class__instructor=user
                ).select_related('fitness_class__instructor').order_by('-id')
            else:
                bookings = Booking.objects.filter(
                    user_id=user
                ).select_related('fitness_class__instructor').order_by('-id')

            paginator = Paginator(bookings, limit)
            paginated_bookings = pagination(page, paginator)

            result = []

            for booking in paginated_bookings:
                cls = booking.fitness_class

                if not cls.date or not cls.time:
                    continue

                instructor_tz = getattr(cls.instructor, 'timezone', 'UTC')

                if instructor_tz in pytz.all_timezones:
                    converted = convert_timezone(
                        date_str=cls.date.strftime("%Y-%m-%d"),
                        time_str=cls.time.strftime("%H:%M:%S"),
                        duration_minutes=cls.duration,
                        current_tz_str=instructor_tz,
                        target_tz_str=user_timezone
                    )
                    date = converted["converted_date"]
                    start_time = converted["converted_start_time"]
                    end_time = converted["converted_end_time"]
                else:
                    start_dt = datetime.combine(cls.date, cls.time)
                    end_dt = start_dt + timedelta(minutes=cls.duration)
                    date = cls.date.strftime("%Y-%m-%d")
                    start_time = cls.time.strftime("%H:%M:%S")
                    end_time = end_dt.time().strftime("%H:%M:%S")

                serialized = BookingSerializer(booking).data
                serialized["fitness_class"]["date"] = date
                serialized["fitness_class"]["start_time"] = start_time
                serialized["fitness_class"]["end_time"] = end_time

                result.append(serialized)

            return handle_ok("Bookings fetched successfully.", result, page, paginator)

        except Exception as err:
            return handle_internal_server_error("Failed to fetch bookings", err)


        
    def post(self, request):
        try:
            if request.user.role != CustomUser.Roles.USER:
                return handle_forbidden("Only users are allowed to create bookings.")

            user_id = request.user.id
            class_id = request.data['fitness_class']
            new_class = FitnessClass.objects.filter(id=class_id).first()

            if not new_class:
                return Response({"error": "Fitness class not found."}, status=status.HTTP_404_NOT_FOUND)

            new_start = datetime.combine(new_class.date, new_class.time)
            new_end = new_start + timedelta(minutes=new_class.duration)

            existing_bookings = Booking.objects.filter(user_id=request.user).select_related('fitness_class')
            for booking in existing_bookings:
                existing_class = booking.fitness_class
                exist_start = datetime.combine(existing_class.date, existing_class.time)
                exist_end = exist_start + timedelta(minutes=existing_class.duration)

                if new_start < exist_end and new_end > exist_start:
                    return Response({
                        "message": (
                            f"You already have a booking from "
                            f"{exist_start.strftime('%I:%M %p')} to {exist_end.strftime('%I:%M %p')}."
                        )
                    }, status=status.HTTP_400_BAD_REQUEST)

            data = request.data.copy()
            data["user_id"] = str(user_id)
            print(data)
            serializer = BookingSerializerCreate(data=data)
            if serializer.is_valid():
                serializer.save()
                return handle_create("Booking")

            return handle_Bad_request(serializer.errors)

        except Exception as err:
            return handle_internal_server_error("Failed to create booking", err)


class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        try:
            if request.user.role != CustomUser.Roles.USER:
                return handle_forbidden("Only USER are allowed to create fitness classes.")
                
            booking = Booking.objects.get(id=id)

            booking.delete()
            return handle_ok("Booking deleted successfully.")

        except Booking.DoesNotExist:
            return handle_not_found("Booking not found or already deleted")

        except Exception as Err:
            return handle_internal_server_error("Failed to delete booking", Err)
