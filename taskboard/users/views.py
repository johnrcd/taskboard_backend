
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

class LoginStatusAPI(APIView):
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)  