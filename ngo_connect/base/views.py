from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from base.models import ngousers, Notifications
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.


def home_base(request):
    return render(request, 'base_home.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        email=request.POST['email']
        username = email
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        pincode = request.POST['pincode']
        user_type = request.POST['selectedOption']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            else:
                # create user and profile objects
                user = User.objects.create_user(
                    username=username, password=password, first_name=first_name,email=email)
                user.save()
                profile = ngousers.objects.create(
                    user=user, phone_number=phone_number, address=address, pincode=pincode, user_type=user_type)
                profile.save()

                messages.success(request, 'Account created successfully.')
                return render(request, 'signup.html')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('signup')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        selected_option = request.POST.get('selectedOption') 


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
                if selected_option == "NGO":
                    if status.user_type == "NGO":
                        return HttpResponseRedirect(reverse("ngo_base"))
                    else:
                        messages.info(request, "You are not an NGO")
                        return render(request, "signup.html")
                elif selected_option == "Donor":
                    if status.user_type == "Donor":
                        return HttpResponseRedirect(reverse("donor_base"))
                    else:
                        messages.info(request, "You are not a donor")
                        return render(request, "signup.html")
                elif selected_option == "Receiver":
                    if status.user_type == "Receiver":
                        return HttpResponseRedirect(reverse("receiver_base"))
                    else:
                        messages.info(request, "You are not a receiver")
                        return render(request, "signup.html")
                else:
                    messages.error(request, "Error")
                    return render(request, 'signup.html')
        else:
            messages.error(request, "Password/email incorrect")
            return render(request, 'signup.html')
        

def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successfull!")
    return render(request, 'signup.html')


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)