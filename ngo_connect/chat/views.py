from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from base.models import ngousers, Notifications
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def home_chat(request):
    return render(request, 'home_chat.html')