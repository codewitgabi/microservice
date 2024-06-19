from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "date_created", "completed", "last_updated"]
    list_filter = ["date_created", "last_updated", "completed", "user"]
    search_fields = ["title", "description"]
    ordering = ["title", "date_created", "completed"]
    list_per_page = 25
    