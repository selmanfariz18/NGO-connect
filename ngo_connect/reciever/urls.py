from django.urls import path
from reciever import views

urlpatterns = [
    path('receiver_login/', views.receiver_login, name='receiver_login'),
    path('receiver_base/', views.receiver_base, name="receiver_base"),
]