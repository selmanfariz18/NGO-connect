from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers
from django.contrib.auth.models import User
from base.models import ngousers, Notifications
from reciever.models import ReceiverMoreDetails
from ngo.models import Reciever_under_ngo, NgoBank


# Create your views here.


@login_required(login_url="signup")
def ngo_base(request):
    # view to load ngo_base page
    user_name=request.user
    users = User.objects.all()
    user_details = ngousers.objects.all()
    reciever = ReceiverMoreDetails.objects.all()
    reciever_ngo = Reciever_under_ngo.objects.all()
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

    notifications = Notifications.objects.filter(user=request.user)
    notification_count = notifications.count()

    balance = ngousers.objects.get(user=request.user)

    # print(balance.is_balance_defined)

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