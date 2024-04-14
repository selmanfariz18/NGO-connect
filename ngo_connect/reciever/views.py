from datetime import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers, Notifications
from django.contrib.auth.models import User
from reciever.models import ReceiverMoreDetails, ReceiverMoreDetails
from django.http import Http404
from ngo.models import NgoBankTransactions, Reciever_under_ngo
from reciever.models import RecieverBank




# Create your views here.


@login_required(login_url="signup")
def receiver_base(request):
    # view to load reciever_base page
    users = ngousers.objects.all()
    try:
        receiver = ReceiverMoreDetails.objects.get(user=request.user)
    except ReceiverMoreDetails.DoesNotExist:
        receiver = ReceiverMoreDetails(user=request.user)

    try:
        ngo = Reciever_under_ngo.objects.get(reciever=request.user)
    except Reciever_under_ngo.DoesNotExist:
        ngo = Reciever_under_ngo(reciever=request.user)

    try:
        reciever_balance = RecieverBank.objects.get(user=request.user)
    except RecieverBank.DoesNotExist:
        reciever_balance = RecieverBank(user=request.user)

        # reciever_balance.current_balance = bank_balance
        # reciever_balance.save()

    notifications = Notifications.objects.filter(user=request.user).order_by('-id')
    notification_count = notifications.count()
    transactions = NgoBankTransactions.objects.filter(to_user=request.user).order_by('-done_at')

    context = {
        'users' : users,
        'reciever' : receiver,
        'ngo' : ngo,
        'reciever_balance' : reciever_balance,
        'notifications' : notifications,
        'notification_count' : notification_count,
        'transactions' : transactions,
    }

    # for user in users:
    #     if user.user_type == 'NGO':
    #         print(user.user.first_name)


    return render(request, 'receiver_base.html', context)

def reciever_type(request):
    # view to set a reciever type
    if request.method == 'POST':
        reciever_type = request.POST.get("options")
        if reciever_type == "other":
            reciever_type = request.POST.get("other_value")
        bank_balance = request.POST.get("bank_balance")

        # print(reciever_type)
        try:
            reciever = ReceiverMoreDetails.objects.get(user=request.user)
        except ReceiverMoreDetails.DoesNotExist:
            reciever = ReceiverMoreDetails(user=request.user)
        reciever.reciever_type = reciever_type
        reciever.is_reciever_type_defined = True
        reciever.save()


        try:
            reciever_balance = RecieverBank.objects.get(user=request.user)
        except RecieverBank.DoesNotExist:
            reciever_balance = RecieverBank(user=request.user)

        reciever_balance.current_balance = bank_balance
        reciever_balance.save()

        #notification sending
        notification = Notifications.objects.create(
            user=request.user,
            name="Details Updated",
            desc="Reciever type and bank balance updated",
        )
        notification.save()


        return HttpResponseRedirect(reverse("receiver_base"))

def reciever_ngo(request):
    # view to sent a request to ngo and make status as pending
    if request.method == 'POST':
        reciever_ngo_email = request.POST.get("reciever_ngo")
        reciever_user = User.objects.get(email=reciever_ngo_email)  # This user is the intended receiver.
        
        try:
            rec = Reciever_under_ngo.objects.get(reciever=request.user)
        except Reciever_under_ngo.DoesNotExist:
            rec = Reciever_under_ngo(reciever=request.user)
        # rec = get_object_or_404(Reciever_under_ngo, reciever=request.user)

        rec.user= reciever_user
        rec.reciever = request.user  # Correctly assign the receiver user.
        rec.status = 'pending'
        rec.save()

        return HttpResponseRedirect(reverse("receiver_base"))
    
def dlt_notification(request):
    """for deleting single notifications."""
    if request.method == 'POST':
        id = request.POST['id']
        notification = get_object_or_404(Notifications, id=id)
        notification.delete()
        return HttpResponseRedirect(reverse("receiver_base"))
    
def reciever_profile_page(request):
    profile = request.user
    try:
        ngouser = ngousers.objects.get(user=request.user)
    except ngousers.DoesNotExist:
        ngouser = ngousers(user=request.user)
    try:
        bank = RecieverBank.objects.get(user=request.user)
    except RecieverBank.DoesNotExist:
        bank = RecieverBank(user=request.user)
    try:
        reciever_type = ReceiverMoreDetails.objects.get(user=request.user)
    except ReceiverMoreDetails.DoesNotExist:
        reciever_type = ReceiverMoreDetails(user=request.user)


    context = {
        'user' : profile,
        'ngouser' : ngouser,
        'reciever_type' : reciever_type,
        'bank' : bank,
    }

    return render(request, 'reciever_profile_page.html', context)


def make_rec_request(request):
    return render(request, 'make_rec_request.html')