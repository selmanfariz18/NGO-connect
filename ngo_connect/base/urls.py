from django.urls import path
from base import views

urlpatterns = [
    path('',views.home_base, name="home_base"),
    path('signup/', views.signup, name="signup"),
]