from django.urls import path
from ngo import views

urlpatterns = [
    path('ngo_base/', views.ngo_base, name="ngo_base"),
    path('ngo_all_users/', views.ngo_all_users, name="ngo_all_users"),
    path('ngo_donor_users', views.ngo_donor_users, name="ngo_donor_users"),
    path('ngo_join_request/', views.ngo_join_request, name="ngo_join_request"),
    path('accept_request/', views.accept_request, name="accept_request"),
    path('reject_request/', views.reject_request, name="reject_request"),
    path('balance_sett', views.balance_sett, name="balance_sett"),
    path('dlt_notification', views.dlt_notification, name="dlt_notification"),
    path('ngo_profile_page', views.ngo_profile_page, name="ngo_profile_page"),
    path('ngo_balance_sheet', views.ngo_balance_sheet, name="ngo_balance_sheet"),
    path('ngo_donate_btn_request', views.ngo_donate_btn_request, name="ngo_donate_btn_request"),
    path('ngo_donation', views.ngo_donation, name="ngo_donation"),
    path('accept_donation_request', views.accept_donation_request, name="accept_donation_request"),
    path('reject_donation_request', views.reject_donation_request, name="reject_donation_request"),
    path('ngo_reciever_details', views.ngo_reciever_details, name="ngo_reciever_details"),
    path('volunteers', views.volunteers, name="volunteers"),
    path('add_volunteers', views.add_volunteers, name="add_volunteers"),
]