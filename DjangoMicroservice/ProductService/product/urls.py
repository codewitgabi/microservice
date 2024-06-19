from django.urls import path
from . import views


urlpatterns = [
    path("", views.CreateProductView.as_view()),
    path("my/", views.get_user_products),
]
