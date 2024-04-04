from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class NgoBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.IntegerField(null=True)

class NgoBankTransactions(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent', null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received', null=True)
    amount = models.IntegerField(null=True)
    transaction_id = models.CharField(max_length=10, null=True)


class Reciever_under_ngo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ngos')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ngos', unique=True)
    status = models.CharField(max_length=10, choices=(('accepted', 'accepted'), ('rejected', 'rejected'), ('pending', 'pending'),), null=True)
