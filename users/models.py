from django.contrib.auth.models import AbstractUser
from django.db import models

class Farmer(AbstractUser):

    phone = models.CharField(max_length=15)

    location = models.CharField(max_length=200)

    def __str__(self):
        return self.username