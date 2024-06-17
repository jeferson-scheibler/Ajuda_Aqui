# ajuda_aqui/core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
default_priority = 1

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    
CustomUser = get_user_model()
    
class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    PRIORITY_CHOICES = [
        (1, 'Baixa'),
        (2, 'Média'),
        (3, 'Alta'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES)

    def __str__(self):
        return self.task_name
    