from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class NgoBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(null=True)
    last_transaction = models.CharField(max_length=255, null=True)
    transaction_log = models.JSONField(null=True)
