from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers
from django.contrib.auth.models import User
from base.models import ngousers
from reciever.models import ReceiverMoreDetails
from ngo.models import Reciever_under_ngo


# Create your views here.


@login_required(login_url="signup")
def ngo_base(request):

    user_name=request.user
    users = User.objects.all()
    user_details = ngousers.objects.all()
    reciever = ReceiverMoreDetails.objects.all()
    reciever_ngo = Reciever_under_ngo.objects.all()
    count = 1

    context = {
        'me' : user_name,
        'users' : users,
        'user_details' : user_details,
        'count' : count,
        'reciever' : reciever,
        'reciever_ngo' : reciever_ngo,
    }

    return render(request, 'ngo_base.html', context)


def ngo_all_users(request):

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
    if request.method == 'POST':
        id = request.POST['id']
        req = get_object_or_404(Reciever_under_ngo, id=id)
        req.status = "accepted"
        req.save()
        return HttpResponseRedirect(reverse("ngo_join_request"))
    
def reject_request(request):
    if request.method == 'POST':
        id = request.POST['id']
        req = get_object_or_404(Reciever_under_ngo, id=id)
        req.status = "rejected"
        req.save()
        return HttpResponseRedirect(reverse("ngo_join_request"))