from django.urls import path
from .views import available_jobs,application_page,my_applications,employer_jobs,employer_applicants,view_resume,update_application_status, mark_mail_sent, view_job, withdraw_application, recommended_jobs

urlpatterns = [
    path('availableApplications/', available_jobs, name="available_jobs"),
    path('jobApplication/<int:job_id>/', application_page, name="application_page" ),
    path('myApplications/', my_applications, name='my_applications'),
    path('employerJobs/', employer_jobs, name="employer_jobs"),
    path('employerApplicants/<int:job_id>/', employer_applicants, name="employer_applicant_list"),
    path('viewResume/<int:application_id>/', view_resume, name="view_resume"),
    path('updateStatus/<int:application_id>/', update_application_status, name="update_application_status"),
    path('mailSent/<int:applicant_id>/', mark_mail_sent, name="mark_mail_sent"),
    path('viewJob/<int:job_id>/', view_job, name="view_job"),
    path('withdrawApplication/<int:application_id>/', withdraw_application, name="withdraw_application"),
    path('recommendedJobs/', recommended_jobs, name="recommended_jobs"),
]
