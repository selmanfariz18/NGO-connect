from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers
from django.contrib.auth.models import User
from base.models import ngousers


# Create your views here.


@login_required(login_url="signup")
def ngo_base(request):

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

    return render(request, 'ngo_base.html', context)
