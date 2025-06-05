# fitness_store/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import WorkingHour
from .serializers import WorkingHoureSerializer

class WorkingHourList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            working_hour = WorkingHour.objects.get(user=request.user)
        except WorkingHour.DoesNotExist:
            return Response({"detail": "You are not registered as a trainer."}, status=status.HTTP_403_FORBIDDEN)

        serializer = WorkingHoureSerializer(working_hour)
        return Response(serializer.data)
