
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TaskboardUserCreateSerializer

class LoginStatusAPI(APIView):
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)
    
class RegisterAPI(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        message = {}
        is_data_valid = True

        if "username" not in request.data:
            is_data_valid = False
            message["username"] = "Field username has not been set."

        if "password" not in request.data:
            is_data_valid = False
            message["password"] = "Field password has not been set."

        if not is_data_valid:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskboardUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print(serializer.data)
        # don't show unused/private fields like password, groups, and user groups   
        return_data = {}
        return_data["id"]           = serializer.data["id"]
        return_data["username"]     = serializer.data["username"]
        return_data["is_superuser"] = serializer.data["is_superuser"]
        return_data["is_staff"]     = serializer.data["is_staff"]
        return_data["is_active"]    = serializer.data["is_active"]
        return_data["date_joined"]  = serializer.data["date_joined"]

        return Response(data=return_data, status=status.HTTP_201_CREATED)


# https://stackoverflow.com/a/55859751
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer