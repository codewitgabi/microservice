from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import WriteTaskSerializer, Task, TaskSerializer


class TaskCreateView(ListCreateAPIView):
    serializer_class = WriteTaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Task.objects.filter(user=request.user.id)
        serializer = TaskSerializer(queryset, many=True)
        return Response({"data": serializer.data})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)


class TaskRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "task_id"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user.id)
