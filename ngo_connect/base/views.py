from django.shortcuts import render

# Create your views here.


def home_base(request):
    return render(request, 'base_home.html')

def sighup(request):
    return render(request, 'signup.html')