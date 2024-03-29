from django.urls import path
from reciever import views

urlpatterns = [
    path('receiver_base/', views.receiver_base, name="receiver_base"),
    path('reciever_ngo', views.reciever_ngo, name="reciever_ngo"),
    path('reciever_type', views.reciever_type, name="reciever_type"),

]