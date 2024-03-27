from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class ReceiverMoreDetails(models.Model):
    reciever_type = models.CharField(max_length=12, null=True)  # Whether receiver is OLH, Orphanage, etc.
    registered_ngo = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,  # This allows the field to be blank in forms as well.
        related_name='registered_ngos'  # This is optional but recommended for reverse querying.
    )
class RecieverBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(null=True)
    last_transaction = models.CharField(max_length=255, null=True)
    transaction_log = models.JSONField(null=True)
