from django.urls import path
from ngo import views

urlpatterns = [
    path('ngo_base/', views.ngo_base, name="ngo_base"),
    path('ngo_all_users/', views.ngo_all_users, name="ngo_all_users"),
]