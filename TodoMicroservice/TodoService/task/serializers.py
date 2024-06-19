import json
from rest_framework import serializers
from .models import Task

from TodoService.amqp_producer import producer
from TodoService.http_producer import auth_producer


class WriteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ["user", "completed"]
        exclude = ["user", "completed"]

    def create(self, validated_data):
        request = self.context.get("request")
        user_id = request.user.id

        task = Task.objects.create(**validated_data)

        try:
            # get user_email
            user = auth_producer.publish("get_user_data", {"id": user_id})

            # send task email notification

            producer.publish(
                json.dumps(
                    {
                        "action": "send_task_creation_email",
                        "payload": {
                            "email": user.get("email"),
                            "task_title": validated_data.get("title"),
                        },
                    }
                )
            )
        except:
            pass

        return task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["user"]
