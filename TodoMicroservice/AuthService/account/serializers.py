import json
from random import randint
from django.contrib.auth import get_user_model
from rest_framework import serializers
from AuthService.producer import producer

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # call email service to send email

        producer.publish(
            json.dumps(
                {
                    "action": "send_account_verification_email",
                    "payload": {
                        "email": validated_data.get("email"),
                        "otp": randint(11111, 99999),
                    },
                }
            )
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
