from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from pytz import all_timezones
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from common.helper.success_message import  *
from common.helper.error_message import  *

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
                    return handle_Bad_request("Timezone is required for users")
                
            tz_value = data.get("timezone")
            if tz_value not in all_timezones:
                return handle_Bad_request(f"{tz_value} is not a valid timezone")

            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return handle_create("User registered")
            return handle_Bad_request(serializer.errors)
        
        except Exception as Err:
            return handle_internal_server_error("Error",Err)

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  
            handle_ok("Logout successful")
            
        except Exception as Err:
            handle_internal_server_error("Error",Err)