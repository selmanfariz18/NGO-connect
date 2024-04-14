from django.urls import path
from reciever import views

urlpatterns = [
    path('receiver_base/', views.receiver_base, name="receiver_base"),
    path('reciever_ngo', views.reciever_ngo, name="reciever_ngo"),
    path('reciever_type', views.reciever_type, name="reciever_type"),
    path('dlt_notification', views.dlt_notification, name="dlt_notification"),
    path('reciever_profile_page', views.reciever_profile_page, name="reciever_profile_page"),
    path('make_rec_request', views.make_rec_request, name="make_rec_request"),
]