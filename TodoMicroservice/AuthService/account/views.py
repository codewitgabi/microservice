from typing import Self
from django.http import HttpRequest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUserSerializer, LoginSerializer, User, UserSerializer


class RegisterUserView(APIView):
    def post(self: Self, request: HttpRequest):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self: Self, request: HttpRequest):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if not User.objects.filter(email=email).exists():
            raise ParseError("No user associated with email")

        user = User.objects.get(email=email)

        if not user.check_password(password):
            raise ParseError("Incorrect password")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
            status=status.HTTP_200_OK,
        )


class UserDetail(APIView):
    def get(self, request: HttpRequest, user_id: int):
        queryset = User.objects.get(id=user_id)
        serializer = UserSerializer(queryset)
        
        return Response({"data": serializer.data})
