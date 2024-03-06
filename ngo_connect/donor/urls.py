from django.urls import path
from donor import views

urlpatterns = [
    path('donor_base/', views.donor_base, name="donor_base"),
]