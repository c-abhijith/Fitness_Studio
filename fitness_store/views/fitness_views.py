from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fitness_store.models import FitnessClass
from fitness_store.serializers import FitnessClassSerializer
from django.utils.timezone import now
from user.models import CustomUser
from common.helper.error_message import *
from common.helper.success_message import *
import pytz
from common.helper.utils import convert_timezone
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated


class FitnessClassListCreateView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            user_timezone = request.query_params.get('timezone') or getattr(request.user, 'timezone', 'UTC')

            if user_timezone not in pytz.all_timezones:
                return handle_Bad_request("Invalid timezone provided.")

            classes = FitnessClass.objects.all()
            result = []

            for cls in classes:
                if not cls.date or not cls.time:
                    continue

                instructor_tz_name = getattr(cls.instructor, 'timezone', None)

                if instructor_tz_name and instructor_tz_name in pytz.all_timezones:
                    converted = convert_timezone(
                        date_str=cls.date.strftime("%Y-%m-%d"),
                        time_str=cls.time.strftime("%H:%M:%S"),
                        duration_minutes=cls.duration,
                        current_tz_str=instructor_tz_name,
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

                serialized = FitnessClassSerializer(cls).data

                serialized["date"] = date
                serialized["start_time"] = start_time
                serialized["end_time"] = end_time

                result.append(serialized)

            return handle_ok("Fitness classes fetched successfully.", result)

        except Exception as err:
            return handle_internal_server_error("An unexpected error occurred", err)

    def post(self, request):
        try:
            if request.user.role != CustomUser.Roles.INSTRUCTOR:
                return handle_forbidden("Only instructors are allowed to create fitness classes.")
            
            data = request.data.copy()
            data['instructor'] = str(request.user.id)

            class_date = data.get('date')
            class_time = data.get('time')
            duration = int(data.get('duration'))

            start_datetime = datetime.strptime(f"{class_date} {class_time}", "%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + timedelta(minutes=duration)

            existing_classes = FitnessClass.objects.filter(instructor=request.user, date=class_date)

            for cls in existing_classes:
                existing_start = datetime.combine(cls.date, cls.time)
                existing_end = existing_start + timedelta(minutes=cls.duration)
                if start_datetime < existing_end and end_datetime > existing_start:
                    return Response({
                        "message": (
                            f"You already have a class '{cls.name}' from "
                            f"{existing_start.strftime('%I:%M %p')} to {existing_end.strftime('%I:%M %p')}."
                        )
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer = FitnessClassSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return handle_create("Fitness class")
            return handle_Bad_request(serializer.errors)

        except Exception as Err:
            return handle_internal_server_error("Failed to create class.", Err)
