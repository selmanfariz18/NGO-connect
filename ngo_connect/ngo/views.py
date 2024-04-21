from django.db import IntegrityError
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers
from django.contrib.auth.models import User
from base.models import ngousers, Notifications
from reciever.models import ReceiverMoreDetails, RecieverBank, RecieverRequests
from ngo.models import NgoBankTransactions, Reciever_under_ngo, NgoBank

import base64
import uuid



# Create your views here.


@login_required(login_url="signup")
def ngo_base(request):
    # view to load ngo_base page
    user_name=request.user
    users = User.objects.all()
    user_details = ngousers.objects.all()
    reciever = ReceiverMoreDetails.objects.all()
    reciever_ngo = Reciever_under_ngo.objects.all()
    reciever_bank = RecieverBank.objects.all()
    count = 1
    ngo_request_count = Reciever_under_ngo.objects.filter(user=request.user, status='pending')
    ngo_request_oah_count = Reciever_under_ngo.objects.filter(
        user=request.user,
        status='accepted',
        reciever__receivermoredetails__reciever_type='OAH'  # Spanning relationships
    ).distinct().count()
    ngo_request_orphanage_count = Reciever_under_ngo.objects.filter(
        user=request.user,
        status='accepted',
        reciever__receivermoredetails__reciever_type='orphanage'  # Spanning relationships
    ).distinct().count()
    ngo_request_non_oah_orphanage_count = Reciever_under_ngo.objects.filter(
        user=request.user,
        status='accepted'
    ).exclude(
        reciever__receivermoredetails__reciever_type__in=['OAH', 'orphanage']
    ).distinct().count()

    # print(ngo_request_non_oah_orphanage_count)

    # bank = NgoBank.objects.get(user=request.user)
    try:
        bank = NgoBank.objects.get(user=request.user)
    except NgoBank.DoesNotExist:
        bank = NgoBank(user=request.user)


    notifications = Notifications.objects.filter(user=request.user).order_by('-id')
    notification_count = notifications.count()

    balance = ngousers.objects.get(user=request.user)

    # print(balance.is_balance_defined)
    reciever_requests = RecieverRequests.objects.filter(to_user=request.user)

    context = {
        'me' : user_name,
        'users' : users,
        'user_details' : user_details,
        'count' : count,
        'reciever' : reciever,
        'reciever_ngo' : reciever_ngo,
        'ngo_request_count' : ngo_request_count,
        'ngo_request_oah_count' : ngo_request_oah_count,
        'ngo_request_orphanage_count' : ngo_request_orphanage_count,
        'ngo_request_non_oah_orphanage_count' : ngo_request_non_oah_orphanage_count,
        'bank' : bank,
        'notifications' : notifications,
        'notification_count' : notification_count,
        'balance' : balance,
        'reciever_bank' : reciever_bank,
        'reciever_requests' : reciever_requests
    }

    return render(request, 'ngo_base.html', context)



def ngo_all_users(request):
    # view to load all recievers detail page
    user_name=request.user
    users = User.objects.all()
    user_details = ngousers.objects.all()
    reciever = ReceiverMoreDetails.objects.all()
    count = 1

    context = {
        'user' : user_name,
        'users' : users,
        'user_details' : user_details,
        'count' : count,
        'reciever' : reciever,
    }

    return render(request, 'ngo_all_users.html', context)


def ngo_join_request(request):
    # view to load page cotain request from recievers to join ngo
    reciever_ngo = Reciever_under_ngo.objects.all()
    user_details = ngousers.objects.all()
    reciever = ReceiverMoreDetails.objects.all()

    context = {
        'reciever_ngo' : reciever_ngo,
        'reciever' : reciever,
        'user_details' : user_details,
    }

    return render(request, 'ngo_join_request.html', context)


def accept_request(request): 
    # view to accept a request from reciever  
    if request.method == 'POST':
        id = request.POST['id']
        req = get_object_or_404(Reciever_under_ngo, id=id)
        req.status = "accepted"
        req.save()
        return HttpResponseRedirect(reverse("ngo_join_request"))
    
def reject_request(request):
    # view to reject a request from reciever
    if request.method == 'POST':
        id = request.POST['id']
        req = get_object_or_404(Reciever_under_ngo, id=id)
        req.status = "rejected"
        req.save()
        return HttpResponseRedirect(reverse("ngo_join_request"))
    

def balance_sett(request):
    if request.method == 'POST':
        bank_balance = request.POST['bank_balance']

        try:
            bank = NgoBank.objects.get(user=request.user)
        except NgoBank.DoesNotExist:
            bank = NgoBank(user=request.user)

        bank.current_balance = bank_balance
        bank.save()

        balance = ngousers.objects.get(user=request.user)
        balance.is_balance_defined = True
        balance.save()

        notification = Notifications.objects.create(
            user=request.user,
            name="Details Updated",
            desc="Bank balance updated",
        )
        notification.save()

        return HttpResponseRedirect(reverse("ngo_base"))

def ngo_donor_users(request):
    # view to load all recievers detail page
    user_name=request.user
    users = User.objects.all()
    user_details = ngousers.objects.all()
    count = 1

    context = {
        'user' : user_name,
        'users' : users,
        'user_details' : user_details,
        'count' : count,
    }

    return render(request, 'ngo_donors.html', context)


def dlt_notification(request):
    """for deleting single notifications."""
    if request.method == 'POST':
        id = request.POST['id']
        notification = get_object_or_404(Notifications, id=id)
        notification.delete()
        return HttpResponseRedirect(reverse("ngo_base"))
    

def ngo_profile_page(request):
    profile = request.user
    try:
        ngouser = ngousers.objects.get(user=request.user)
    except ngousers.DoesNotExist:
        ngouser = ngousers(user=request.user)
    try:
        bank = NgoBank.objects.get(user=request.user)
    except NgoBank.DoesNotExist:
        bank = NgoBank(user=request.user)


    context = {
        'user' : profile,
        'ngouser' : ngouser,
        'bank' : bank,
    }

    return render(request, 'ngo_profile_page.html', context)

def ngo_balance_sheet(request):
    profile=request.user

    try:
        bank = NgoBank.objects.get(user=request.user)
    except NgoBank.DoesNotExist:
        bank = NgoBank(user=request.user)

    transactions = NgoBankTransactions.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    ).order_by('-done_at')

    context = {
        'user': profile,
        'bank': bank,
        'transactions': transactions,
    }

    return render(request, 'ngo_balance_sheet.html', context)

def ngo_donate_btn_request(request):
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
        return render(request, 'ngo_donation.html', context)
    
def ngo_donation(request):
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



        # Update recipient's bank balance
        bank, _ = NgoBank.objects.get_or_create(user=from_user)
        if (bank.current_balance-amount) >= 0:
            bank.current_balance = (bank.current_balance or 0) - amount  
            bank.save()

            bank1, _ = RecieverBank.objects.get_or_create(user=to_user)
            bank1.current_balance = (bank1.current_balance or 0) + amount  
            bank1.save()

            try:
                # Directly create a new transaction
                NgoBankTransactions.objects.create(
                    from_user=from_user,
                    to_user=to_user,
                    amount=amount,
                    transaction_id=transaction_id,
                    transaction_type='debited',
                )
            except IntegrityError:
                # Handle the case where the transaction_id is not unique, which should be rare
                pass

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
            messages.success(request, "Payment success")
        else:
            messages.error(request, "Insufficient balance")
            Notifications.objects.create(
                user=from_user,
                name="Insufficient balance",
                desc="Last transaction cancelled due to insufficient balance.",
            )
            return redirect("ngo_base")
            

        return HttpResponseRedirect(reverse("ngo_base"))
    

def accept_donation_request(request):
    if request.method == 'POST':
        to_user = request.POST['to_user']
        r_id = request.POST['id']

        unique_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')
        transaction_id = unique_id[:10]

        # bank, _ = NgoBank.objects.get_or_create(user=request.user)
        rec = RecieverRequests.objects.get(id=r_id)

        if request.POST['amount']:
            amount = int(request.POST['amount'])
            bank, _ = NgoBank.objects.get_or_create(user=request.user)
            if (bank.current_balance-amount) >= 0:
                rec = RecieverRequests.objects.get(id=r_id)
                rec.status = 'accepted'
                rec.save()

                bank.current_balance = (bank.current_balance or 0) - amount  
                bank.save()

                # print(request.user, to_user)

                to_user = get_object_or_404(User, email=to_user)

                bank1, _ = RecieverBank.objects.get_or_create(user=to_user)
                bank1.current_balance = (bank1.current_balance or 0) + amount  
                bank1.save()

                try:
                    # Directly create a new transaction
                    NgoBankTransactions.objects.create(
                        from_user=request.user,
                        to_user=to_user,
                        amount=amount,
                        transaction_id=transaction_id,
                        transaction_type='debited',
                    )
                except IntegrityError:
                    # Handle the case where the transaction_id is not unique, which should be rare
                    pass
                Notifications.objects.create(
                    user=request.user,
                    name="Amount Debited",
                    desc=f"Debited to {to_user.first_name}. Amount is Rs.{amount}",
                )
                Notifications.objects.create(
                    user=to_user,
                    name="Amount Credited",
                    desc=f"Credited from {request.user.first_name}. Amount is Rs.{amount}",
                )
                messages.success(request, "Requested Payment success")

            else:
                messages.error(request, "Insufficient balance to accept request")
                Notifications.objects.create(
                    user=request.user,
                    name="Insufficient balance",
                    desc="Last transaction cancelled due to insufficient balance.",
                )

        else :
            goods_name = int(request.POST['goods_name'])
            count = int(request.POST['count'])
            messages.error(request, "Not ready to accept goods request")


        # print(rec.status)

    return redirect("ngo_base")