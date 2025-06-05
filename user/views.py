from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from common.helper.default_schedule import default_schedule
from pytz import all_timezones


from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data.copy()
            role = data.get("role", CustomUser.Roles.USER)
            timezone = data.get("timezone")

            if role == CustomUser.Roles.INSTRUCTOR:
                if not timezone:
                    data["timezone"] = "Asia/Kolkata"
            elif role == CustomUser.Roles.USER:
                if not timezone:
                    return Response(
                        {"timezone": "Timezone is required for users."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            tz_value = data.get("timezone")
            if tz_value not in all_timezones:
                return Response(
                    {"timezone": f"{tz_value} is not a valid timezone."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()

                return Response({
                    "message": "User registered successfully",
                    "user": RegisterSerializer(user).data
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token or token already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)