from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class ReceiverMoreDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reciever_type = models.CharField(max_length=12, null=True)  # Whether receiver is OLH, Orphanage, etc.
    is_reciever_type_defined = models.BooleanField(default=False)
    
class Ngo_reciever(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_ngo_defined = models.BooleanField(default=False)
    ngo = models.CharField(max_length=12, null=True)


class RecieverBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(null=True)

class RecieverBankTransactions(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions', null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions', null=True)
    current_balance = models.IntegerField(null=True)
    transaction_id = models.CharField(max_length=10, null=True)


class RecieverBankLog(models.Model):
    transaction_id = models.CharField(max_length=10, primary_key=True)
    from_user = models.CharField(max_length=20, null=True)
    to_user = models.CharField(max_length=20, blank=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
