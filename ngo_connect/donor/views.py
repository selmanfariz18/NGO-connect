from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers, Notifications
from django.contrib.auth.models import User
from ngo.models import NgoBankTransactions, NgoBank

import base64
import uuid




# Create your views here.

@login_required(login_url="signup")
def donor_base(request):

    ngos = ngousers.objects.filter(user_type='NGO')

    notifications = Notifications.objects.filter(user=request.user)
    notification_count = notifications.count()

    context = {
        'ngos': ngos,
        'notifications' : notifications,
        'notification_count' : notification_count,
    }

    return render(request, 'donor_base.html', context)


def donate_btn_request(request):
    # view to reject a request from reciever
    if request.method == 'POST':
        id = request.POST['id']
        # user = request.POST['user']
        # req = get_object_or_404(User, id=id)

        

        context = {
            'from_user' : request.user,
            'to_user' : id,
        }

        print(request.user)
        return render(request, 'donor_donation.html', context)
    

def donation(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        from_user = request.POST['from_user']
        to_user = request.POST['to_user']
        unique_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')
        transaction_id = unique_id[:10]


        from_user = get_object_or_404(User, email=from_user)
        to_user = get_object_or_404(User, email=to_user)
        try:
            transaction = NgoBankTransactions.objects.get(from_user=from_user, to_user=to_user)
        except NgoBankTransactions.DoesNotExist:
            transaction = NgoBankTransactions(from_user=from_user, to_user=to_user)

        transaction.amount = amount
        transaction.transaction_id = transaction_id
        transaction.save()

        try:
            bank = NgoBank.objects.get(user=to_user)
        except NgoBank.DoesNotExist:
            bank = NgoBank(user=request.user)

        bank.current_balance = bank.current_balance + amount
        bank.save()

        notification = Notifications.objects.create(
            user=from_user,
            name="Amount Debited",
            desc="Debited to "+str(to_user.first_name)+". Amount is Rs."+str(amount),
        )
        notification.save()

        notification = Notifications.objects.create(
            user=to_user,
            name="Amount Credited",
            desc="Credited from "+str(from_user.first_name)+". Amount is Rs."+str(amount),
        )
        notification.save()


        return HttpResponseRedirect(reverse("donor_base"))



        
