from django.shortcuts import render, get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    TaskboardUserCreateSerializer,
    TaskboardUserProfileSerializer,
    TaskboardUserModificationSerializer,
)
from .models import TaskboardUser

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


class ProfileViewSet(viewsets.ViewSet):
    lookup_field = "username"
    permission_classes=(IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, username=None):
        """Returns a single user."""

        user = get_object_or_404(TaskboardUser.objects.all(), username=username)
        serializer = TaskboardUserProfileSerializer(user)
        return Response(serializer.data)
    
    # i just copied directly from the source. seems to be boilerplate tbh
    # https://www.cdrf.co/3.14/rest_framework.viewsets/ModelViewSet.html#partial_update
    def partial_update(self, request, username=None, *args, **kwargs):
        """Partially updates a user."""

        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def update(self, request, username=None, *args, **kwargs):
        """Updates a user's fields."""

        # forcing PATCH and PUT to act the same because i don't care
        # about the nuances between them

        # partial = kwargs.pop('partial', False)
        partial = True

        if username != request.user.username:
            content = {
                "error": "Cannot update user profile of " + \
                str(request.data["username"]) + " because request is " + \
                "authenticated as " + str(request.user.username) + ". " + \
                "Users cannot update other profiles."
            }
            return Response(data=content, status=status.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(TaskboardUser.objects.all(), username=request.user.username)
        serializer = TaskboardUserProfileSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # i don't know what this does but the api documentation had this
        # https://www.cdrf.co/3.14/rest_framework.viewsets/ModelViewSet.html#update
        if getattr(user, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            user._prefetched_objects_cache = {}

        return Response(serializer.data)

    
@api_view(["GET"])
def view_profile(request, username):
    user = get_object_or_404(TaskboardUser.objects.all(), username=username)
    serializer = TaskboardUserProfileSerializer(user)
    return Response(serializer.data)

# https://stackoverflow.com/a/55859751
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer