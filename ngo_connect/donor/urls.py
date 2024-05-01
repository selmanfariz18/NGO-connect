from django.urls import path
from donor import views

urlpatterns = [
    path('donor_base/', views.donor_base, name="donor_base"),
    path('donate_btn_request', views.donate_btn_request, name="donate_btn_request"),
    path('donation', views.donation, name="donation"),
    path('dlt_notification', views.dlt_notification, name="dlt_notification"),
    path('donor_profile_page', views.donor_profile_page, name="donor_profile_page"),
    path('donor_ngo_details', views.donor_ngo_details, name="donor_ngo_details"),
]