from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,JobSeekerProfile

class JobSeekerRegistrationForm(UserCreationForm):
    EXPERIENCE_CHOICES = [
    ("0-1", "0-1 years"),
    ("1-3", "1-3 years"),
    ("3-5", "3-5 years"),
    ("5-10", "5-10 years"),
    ("10+", "10+ years"),
    ]

    EDUCATION_CHOICES = [
        ("high-school", "High School"),
        ("diploma", "Diploma"),
        ("bachelor", "Bachelor's Degree"),
        ("master", "Master's Degree"),
        ("phd", "PhD"),
        ("other", "Other"),
    ]

    phone_number = forms.CharField(max_length=15)
    profession = forms.CharField()
    experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES)
    education = forms.ChoiceField(choices=EDUCATION_CHOICES)
    skills = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Seperate skills by comma (,)"}))
    resume = forms.FileField()
    cover_letter = forms.CharField(widget=forms.Textarea,required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password1','password2']


class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField()
    company_website = forms.CharField()
    company_location = forms.CharField()
    contact_number = forms.CharField()
    company_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password1','password2']

class EmailLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class JobSeekerProfileForm(forms.ModelForm):
    
    class Meta:
        model = JobSeekerProfile
        fields = ['phone_number', 'profession', 'education', 'skills', 'experience', 'resume']
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': "Seperate skills by comma (,)"}),
        }

    