# jobs/urls.py

from django.urls import path
from .views import post_job,employer_job_list,edit_job,delete_job

urlpatterns = [
    path('jobPost/', post_job, name="job_post"),
    path('employerJobList/', employer_job_list, name="employer_job_list" ),
    path('editJob/<int:job_id>/', edit_job, name="edit_job"),
    path('deleteJob/<int:job_id>/', delete_job, name="delete_job"),
]
