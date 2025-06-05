from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fitness_store.models import Booking, FitnessClass
from fitness_store.serializers import BookingSerializer
from user.models import CustomUser
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import datetime, timedelta
from common.helper.error_message import *
from common.helper.success_message import *
from common.helper.pagination import pagination
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated


class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            page = request.GET.get("page", 1)
            limit = request.GET.get("limit", 20)
            bookings = Booking.objects.filter(user_id=request.user)
            paginator = Paginator(bookings, limit)
            result = pagination(page, paginator)
            serializer = BookingSerializer(result, many=True)
            return handle_ok("Bookings fetched successfully.", serializer.data, page, paginator)

        except Exception as Err:
            return handle_internal_server_error("Failed to fetch bookings", Err)

    def post(self, request):
        try:
            if request.user.role != CustomUser.Roles.USER:
                return handle_forbidden("Only USER are allowed to create fitness classes.")

            user = request.user
            class_id = request.data.get('fitness_class')
            new_class = FitnessClass.objects.filter(id=class_id).first()

            if not new_class:
                return Response({"error": "Fitness class not found."}, status=status.HTTP_404_NOT_FOUND)

            new_start = datetime.combine(new_class.date, new_class.time)
            new_end = new_start + timedelta(minutes=new_class.duration)

            existing_bookings = Booking.objects.filter(user_id=user).select_related('fitness_class')

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

            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=user)
                return handle_create("Booking")
            return handle_Bad_request(serializer.errors)

        except Exception as Err:
            return handle_internal_server_error("Failed to create booking", Err)


class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, booking_id, user):
        return get_object_or_404(Booking, id=booking_id, user_id=user)

    def get(self, request, id):
        try:
            booking = self.get_object(id, request.user)
            serializer = BookingSerializer(booking)
            return handle_ok("Booking retrieved successfully", serializer.data)
        except Exception as Err:
            return handle_internal_server_error("Failed to retrieve booking", Err)

    def delete(self, request, id):
        try:
            if request.user.role != CustomUser.Roles.USER:
                return handle_forbidden("Only USER are allowed to create fitness classes.")
                
            booking = self.get_object(id, request.user)
            class_start = datetime.combine(booking.fitness_class.date, booking.fitness_class.time)

            if class_start - now() < timedelta(hours=12):
                return handle_Bad_request("You can only delete a booking at least 12 hours before the class starts")

            booking.delete()
            return handle_ok("Booking deleted successfully.")

        except Booking.DoesNotExist:
            return handle_not_found("Booking not found or already deleted")

        except Exception as Err:
            return handle_internal_server_error("Failed to delete booking", Err)
