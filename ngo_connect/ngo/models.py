from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class NgoBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(null=True)
    last_transaction = models.CharField(max_length=255, null=True)
    transaction_log = models.JSONField(null=True)

class Reciever_under_ngo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Specify a unique related_name for this ForeignKey
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ngo_recievers', null=True)
    status = models.CharField(max_length=10, choices=(('accepted', 'accepted'), ('rejected', 'rejected'), ('pending', 'pending'),), null=True)
