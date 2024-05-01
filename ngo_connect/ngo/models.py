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
    transaction_type = models.CharField(max_length=8, choices=(('credited', 'credited'), ('debited', 'debited')), null=True)
    done_at = models.DateTimeField(auto_now=True,blank=True, null=True)


class Reciever_under_ngo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ngos')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ngos', unique=True)
    status = models.CharField(max_length=10, choices=(('accepted', 'accepted'), ('rejected', 'rejected'), ('pending', 'pending'),), null=True)

class NgoVolunteers(models.Model):
    ngo = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=8, choices=(('male', 'male'), ('female', 'female'),), null=True)
    job = models.CharField(max_length=20, blank=True)