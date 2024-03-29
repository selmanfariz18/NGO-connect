from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers
from django.contrib.auth.models import User



# Create your views here.


@login_required(login_url="signup")
def receiver_base(request):

    users = ngousers.objects.all()

    context = {
        'users' : users,
    }

    # for user in users:
    #     if user.user_type == 'NGO':
    #         print(user.user.first_name)


    return render(request, 'receiver_base.html', context)

def reciever_ngo(request):
    if request.method == 'POST':
        reciever_ngo = request.POST.get("reciever_ngo")

        print(reciever_ngo)
        return HttpResponseRedirect(reverse("receiver_base"))