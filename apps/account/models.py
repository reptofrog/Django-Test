from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    job_title = models.CharField(max_length=40, unique=True)
