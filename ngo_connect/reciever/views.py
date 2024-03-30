from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers
from django.contrib.auth.models import User
from reciever.models import ReceiverMoreDetails
from django.http import Http404
from ngo.models import Reciever_under_ngo




# Create your views here.


@login_required(login_url="signup")
def receiver_base(request):

    users = ngousers.objects.all()
    try:
        receiver = ReceiverMoreDetails.objects.get(user=request.user)
    except ReceiverMoreDetails.DoesNotExist:
        receiver = ReceiverMoreDetails(user=request.user)

    try:
        ngo = Reciever_under_ngo.objects.get(reciever=request.user)
    except Reciever_under_ngo.DoesNotExist:
        ngo = Reciever_under_ngo(reciever=request.user)

    context = {
        'users' : users,
        'reciever' : receiver,
        'ngo' : ngo,
    }

    # for user in users:
    #     if user.user_type == 'NGO':
    #         print(user.user.first_name)


    return render(request, 'receiver_base.html', context)

def reciever_type(request):
    if request.method == 'POST':
        reciever_type = request.POST.get("options")
        if reciever_type == "other":
            reciever_type = request.POST.get("other_value")

        # print(reciever_type)
        try:
            reciever = ReceiverMoreDetails.objects.get(user=request.user)
        except ReceiverMoreDetails.DoesNotExist:
            reciever = ReceiverMoreDetails(user=request.user)
        reciever.reciever_type = reciever_type
        reciever.is_reciever_type_defined = True
        reciever.save()

        return HttpResponseRedirect(reverse("receiver_base"))

def reciever_ngo(request):
    if request.method == 'POST':
        reciever_ngo_email = request.POST.get("reciever_ngo")
        reciever_user = User.objects.get(email=reciever_ngo_email)  # This user is the intended receiver.

        # try:
        #     reciever = Reciever_under_ngo.objects.get(user=request.user)
        # except Reciever_under_ngo.DoesNotExist:
        #     reciever = Reciever_under_ngo(user=request.user)
        
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
