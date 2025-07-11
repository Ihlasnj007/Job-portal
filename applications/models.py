from django.db import models
from jobs.models import JobPost
from accounts.models import JobSeekerProfile

# Create your models here.

class ApplicationPage(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    mail_sent = models.BooleanField(default=False)