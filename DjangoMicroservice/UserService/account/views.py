from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterUserSerializer


class RegisterUserView(APIView):
    def post(self, request: HttpRequest):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
