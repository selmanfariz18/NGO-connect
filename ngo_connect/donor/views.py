from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers


# Create your views here.

@login_required(login_url="signup")
def donor_base(request):
    return render(request, 'donor_base.html')
