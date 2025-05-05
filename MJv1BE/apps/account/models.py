# account/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')