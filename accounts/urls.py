# accounts/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Jobseeker_Register,Employer_Register,login_view,employer_dashboard,jobseeker_dashboard,my_profile,edit_profile

urlpatterns = [
    path('registerJobseeker/', Jobseeker_Register ,name='jobseeker_register'),
    path('registerEmployer/', Employer_Register, name='employer_register'),
    path('login/', login_view, name='login'),
    path('employerDashboard/', employer_dashboard, name='employer_dashboard'),
    path('jobseekerDashboard/', jobseeker_dashboard, name='jobseeker_dashboard'),
    path('myProfile/', my_profile, name='my_profile'),
    path('editProfile/', edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
