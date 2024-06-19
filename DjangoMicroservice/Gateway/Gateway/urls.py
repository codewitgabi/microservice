from django.contrib import admin
from django.urls import path
from .app import api


urlpatterns = [
    path("", api.urls)
]
