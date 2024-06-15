# ajuda_aqui/core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    
CustomUser = get_user_model()
    
class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, default=None)
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()

    def __str__(self):
        return self.task_name