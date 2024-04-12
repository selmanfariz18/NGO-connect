from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
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
    # Fetch all NGO users
    ngos = ngousers.objects.filter(user_type='NGO')

    # Prepare a list to hold NGO data with bank balance
    ngos_with_balance = []
    for ngo in ngos:
        # Try to fetch the NgoBank object associated with the current user
        ngo_bank = NgoBank.objects.filter(user=ngo.user).first()
        # If there is an associated NgoBank object, fetch the balance, else set to None
        ngo_bank_balance = ngo_bank.current_balance if ngo_bank else None
        # Append the NGO and its bank balance to the list
        ngos_with_balance.append({
            'ngo': ngo,
            'bank_balance': ngo_bank_balance,
        })

    notifications = Notifications.objects.filter(user=request.user).order_by('-id')
    notification_count = notifications.count()

    transactions = NgoBankTransactions.objects.filter(from_user=request.user).order_by('-done_at')

    context = {
        'ngos_with_balance': ngos_with_balance,
        'notifications': notifications,
        'notification_count': notification_count,
        'transactions' : transactions,
    }

    return render(request, 'donor_base.html', context)


def donate_btn_request(request):
    # view to reject a request from reciever
    if request.method == 'POST':
        id = request.POST['id']
        # user = request.POST['user']
        # req = get_object_or_404(User, id=id)

        ngo_user = get_object_or_404(ngousers, id=id).user

        context = {
            'from_user' : request.user.email,
            'to_user' : ngo_user.email,
        }

        # print(user)
        return render(request, 'donor_donation.html', context)
    

def donation(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])  # Convert amount to integer
        from_user_email = request.POST['from_user']
        to_user_email = request.POST['to_user']

        # Get User objects for both donor and recipient
        from_user = get_object_or_404(User, email=from_user_email)
        to_user = get_object_or_404(User, email=to_user_email)

        # Generate a unique transaction ID
        unique_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')
        transaction_id = unique_id[:10]

        try:
            # Directly create a new transaction
            NgoBankTransactions.objects.create(
                from_user=from_user,
                to_user=to_user,
                amount=amount,
                transaction_id=transaction_id,
                transaction_type='credited',
            )
        except IntegrityError:
            # Handle the case where the transaction_id is not unique, which should be rare
            pass

        # Update recipient's bank balance
        bank, _ = NgoBank.objects.get_or_create(user=to_user)
        bank.current_balance = (bank.current_balance or 0) + amount  # Ensure there's a default value
        bank.save()

        # Create notifications for both parties
        Notifications.objects.create(
            user=from_user,
            name="Amount Debited",
            desc=f"Debited to {to_user.first_name}. Amount is Rs.{amount}",
        )
        Notifications.objects.create(
            user=to_user,
            name="Amount Credited",
            desc=f"Credited from {from_user.first_name}. Amount is Rs.{amount}",
        )

        return HttpResponseRedirect(reverse("donor_base"))

def dlt_notification(request):
    """for deleting single notifications."""
    if request.method == 'POST':
        id = request.POST['id']
        notification = get_object_or_404(Notifications, id=id)
        notification.delete()
        return HttpResponseRedirect(reverse("donor_base"))

def donor_profile_page(request):
    profile = request.user
    try:
        ngouser = ngousers.objects.get(user=request.user)
    except ngousers.DoesNotExist:
        ngouser = ngousers(user=request.user)
    # try:
    #     bank = NgoBank.objects.get(user=request.user)
    # except NgoBank.DoesNotExist:
    #     bank = NgoBank(user=request.user)


    context = {
        'user' : profile,
        'ngouser' : ngouser,
        # 'bank' : bank,
    }

    return render(request, 'donor_profile_page.html', context)


        
