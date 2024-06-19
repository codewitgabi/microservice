import json
from typing import Self
from django.http import HttpRequest
from rest_framework.permissions import BasePermission
from ProductService.producer import producer


class IsAuthenticated(BasePermission):
    """
    New permission to check if a user is authenticated since we are using a microservice architecture.
    """

    def has_permission(self: Self, request: HttpRequest, view):
        headers = request.headers

        if "Authorization" not in headers:
            return False

        bearer, token = headers.get("Authorization").split()

        if bearer != "Bearer":
            return False

        result = producer.publish(
            {"action": "authenticate", "data": json.dumps({"token": token})}
        )

        if isinstance(result.get("data"), dict):
            request.user = result.get("data")

            return True
        return False
