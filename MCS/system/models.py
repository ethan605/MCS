from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    priority = models.IntegerField()

class Shop(User):
    email = models.EmailField()
    display_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()

class Permission(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    