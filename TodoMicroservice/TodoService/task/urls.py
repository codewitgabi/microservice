from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskCreateView.as_view()),
    path("<int:task_id>/", views.TaskRetrieveUpdateDeleteView.as_view()),
]
