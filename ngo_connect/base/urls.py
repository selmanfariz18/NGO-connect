from django.urls import path
from base import views

urlpatterns = [
    path('',views.home_base, name="home_base"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout_user, name="logout"),
]