from django.urls import path
from ngo import views

urlpatterns = [
    path('ngo_base/', views.ngo_base, name="ngo_base"),
]