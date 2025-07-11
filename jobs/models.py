from django.db import models
from accounts.models import CustomUser

# Create your models here.

class JobPost(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    job_description = models.TextField()
    required_experience = models.CharField(max_length=100)
    required_education = models.CharField(max_length=100)
    required_skills = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    application_method = models.CharField(max_length=100)
    application_deadline = models.DateField()
    additional_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
