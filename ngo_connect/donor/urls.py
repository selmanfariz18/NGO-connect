from django.urls import path
from donor import views

urlpatterns = [
    path('donor_login/', views.donor_login, name='donor_login'),
    path('donor_base/', views.donor_base, name="donor_base"),
]