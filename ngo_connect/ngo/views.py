from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import ngousers


# Create your views here.

def ngo_login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user = authenticate(request=request, username=email, password=password)
        if user is not None:
            login(request=request, user=user)
            try:
                status = ngousers.objects.get(user=request.user)
            except ngousers.DoesNotExist:
                # As a best practice, specify all necessary fields when creating a new object.
                status = ngousers(user=request.user)           
            if user.is_superuser:
                messages.error(request, "Password/email incorrect")
                return render(request, 'signup.html')
            else:
                if status.user_type == "NGO":
                    return HttpResponseRedirect(reverse("ngo_base"))
                else:
                    messages.info(request, "You are not an NGO")
                    return render(request, "signup.html")
        else:
            messages.error(request, "Password/email incorrect")
            return render(request, 'signup.html')


@login_required(login_url="signup")
def ngo_base(request):
    return render(request, 'ngo_base.html')
