from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class Shop(User):
    display_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()