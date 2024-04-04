from django.urls import path
from donor import views

urlpatterns = [
    path('donor_base/', views.donor_base, name="donor_base"),
    path('donate_btn_request', views.donate_btn_request, name="donate_btn_request"),
    path('donation', views.donation, name="donation"),
]