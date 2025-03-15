# accounts/models.py  

from django.contrib.auth.models import AbstractUser  
from django.db import models  

class CustomUser(AbstractUser):  
    USER_TYPE_CHOICES = (  
        (1, 'Customer'),  
        (2, 'Apartment Manager'),  
    )  
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)  