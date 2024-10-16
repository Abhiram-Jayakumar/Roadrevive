from django.db import models

from Employee.models import Employee

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)




class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Road Damage', 'Road Damage'),
        ('Potholes', 'Potholes'),
        ('Drainage Issues', 'Drainage Issues'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Work agreed', 'Work agreed'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)  
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True) 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES) 
    description = models.TextField()  
    location = models.CharField(max_length=150)
    landmark = models.CharField(max_length=150)
    pin = models.CharField(max_length=8)
    image = models.ImageField(upload_to='complaints/', null=True, blank=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  
    date_filed = models.DateTimeField(auto_now_add=True) 
    feedback = models.TextField(null=True, blank=True) 

