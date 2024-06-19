# ajuda_aqui/core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Adicione campos personalizados se necessário
    pass
