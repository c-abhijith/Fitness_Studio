# fitness_store/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Trainer
from .serializers import TrainerScheduleSerializer

class MyScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            trainer = Trainer.objects.get(user=request.user)
        except Trainer.DoesNotExist:
            return Response({"detail": "You are not registered as a trainer."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TrainerScheduleSerializer(trainer)
        return Response(serializer.data)
