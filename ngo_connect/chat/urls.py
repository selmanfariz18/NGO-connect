from django.urls import path
from chat import views

urlpatterns = [
    path('',views.home_chat, name="home_chat"),
]