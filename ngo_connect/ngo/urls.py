from django.urls import path
from ngo import views

urlpatterns = [
    path('ngo_base/', views.ngo_base, name="ngo_base"),
    path('ngo_all_users/', views.ngo_all_users, name="ngo_all_users"),
    path('ngo_join_request/', views.ngo_join_request, name="ngo_join_request"),
    path('accept_request/', views.accept_request, name="accept_request"),
    path('reject_request/', views.reject_request, name="reject_request"),

]