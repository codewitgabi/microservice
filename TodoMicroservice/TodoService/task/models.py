from django.db import models


class Task(models.Model):
    user = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["title", "completed"])]

    def __str__(self) -> str:
        return self.title
