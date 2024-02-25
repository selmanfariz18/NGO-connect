from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from base.models import ngousers

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
        user_type = request.POST['user_type']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email already exists')
                return redirect('sighup')
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
            return redirect('sighup')

    return render(request, 'signup.html')