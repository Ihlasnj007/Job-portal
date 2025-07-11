from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings

# Create your models here.

# ✅ Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.pop('username', None)  # fallback
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# ✅ CustomUser using AbstractUser
class CustomUser(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)

    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # required when creating superuser

    objects = CustomUserManager()  # ✅ use the custom manager

    def __str__(self):
        return self.email
    
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='jobseeker_profile')
    phone_number = models.CharField(max_length=15,blank=True)
    profession = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    education = models.CharField(max_length=100)
    skills = models.CharField(max_length=300)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s profile"
    
class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=100)
    company_website = models.URLField()
    company_location = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    company_description = models.TextField()

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"