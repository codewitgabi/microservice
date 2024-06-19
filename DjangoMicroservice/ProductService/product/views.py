import json
from typing import Self
from django.http import HttpRequest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError

from .models import Product
from .serializers import ProductSerializer

from .permissions import IsAuthenticated
from ProductService.producer import producer


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self: Self, request: HttpRequest):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"data": serializer.data})

    def post(self: Self, request: HttpRequest):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = producer.publish(
            {
                "action": "is_valid_user_id",
                "data": json.dumps({"vendor": serializer.validated_data.get("vendor")}),
            }
        )

        is_valid_user_id = result.get("data")

        if is_valid_user_id:
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

        raise ParseError("No user associated with the given id")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_products(request: HttpRequest):
    user_id = request.user.get("id")

    products = Product.objects.filter(vendor=user_id)
    serializer = ProductSerializer(products, many=True)
    return Response({"data": serializer.data})
