# tasks/models.py
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Görevi kime ait?
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
