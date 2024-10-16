from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    position = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_joined = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=20)
