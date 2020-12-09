# accounts app views
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from soko.accounts.backends import JWTAuthentication
from soko.accounts.serializers import LoginSerializer
from soko.accounts.serializers import RegistrationSerializer
from helpers.renderers import UserJSONRenderer


class RegisterAPIView(GenericAPIView):
    """View to register a new user"""

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    operation = "Register"

    def post(self, request: Request, **kwargs) -> Response:
        """Post method to register a user"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Hello {}, You have been successfully registered".format(
                    request.data.get("username")
                ),
                "status": "success",
                "data": {
                    "username": request.data.get("username"),
                    "email": request.data.get("email"),
                },
            },
            status=status.HTTP_201_CREATED,
        )

class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    operation = "Login"
    renderer_classes = (UserJSONRenderer,)

    def post(self, request: Request) -> Response:
        """Login a user"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data.get("username", None)
        user = User.objects.get(username=username)
        userdata = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
        token = JWTAuthentication.generate_token(userdata=userdata)
        username = user.username
        email = user.email
        # update user last login
        user.last_login = now()
        user.save()

        return Response(
            {
                "message": "Welcome {}".format(username),
                "status": "success",
                "data": {"token": token, "username": username, "email": email},
            },
            status=status.HTTP_200_OK,
        )