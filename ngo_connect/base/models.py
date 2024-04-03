from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class ngousers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=[
        ('NGO', 'NGO'),
        ('Donor', 'Donor'),
        ('Receiver','Receiver'),
    ])
    phone_number = models.CharField(max_length=13, null=True)
    address = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=10, null=True)

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

