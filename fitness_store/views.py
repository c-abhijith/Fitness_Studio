from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass
from .serializers import FitnessClassSerializer
from django.shortcuts import get_object_or_404

from uuid import UUID
from rest_framework.permissions import IsAuthenticated


class FitnessClassListCreateView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            classes = FitnessClass.objects.all()
            serializer = FitnessClassSerializer(classes, many=True)
            return Response({
                                "message": "Fitness class updated successfully.",
                                "data": serializer.data
                            })

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred while fetching classes: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            data = request.data.copy()
            data['instructor'] = str(request.user.id)  

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
        
