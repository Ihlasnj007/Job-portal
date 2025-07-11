from django import forms
from . models import JobPost

class JobPostForm(forms.ModelForm):
    JobType_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time','Part Time'),
        ('Contract','Contract'),
        ('Internship','Internship'),
    ]

    EXPERIENCE_CHOICES = [
        ('Entry Level','Entry Level'),
        ('Mid Level','Mid Level'),
        ('Senior Level','Senior Level'),
        ('Executive','Executive')
    ]

    EDUCATION_CHOICES = [
        ('High SChool','High SChool'),
        ('Associate Degree','Associate Degree'),
        ('Bachelor\'s Degree','Bachelor\'s Degree'),
        ('Master\'s Degree','Master\'s Degree'),
        ('PhD','PhD')
    ]

    APPLICATION_CHOICES = [
        ('Email Application','Email Application'),
        ('Company Website','Company Website'),
        ('Through This Platform','Through This Platform')
    ]

    job_type = forms.ChoiceField(choices=JobType_CHOICES)
    job_description = forms.CharField(widget=forms.Textarea,required=True)
    required_experience = forms.ChoiceField(choices=EXPERIENCE_CHOICES)
    required_education = forms.ChoiceField(choices=EDUCATION_CHOICES)
    responsibilities = forms.CharField(widget=forms.Textarea, required=False)
    application_method = forms.ChoiceField(choices=APPLICATION_CHOICES)
    application_deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    additional_notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = JobPost
        fields = [
            'job_title', 'job_type', 'location', 'department',
            'job_description', 'required_experience', 'required_education',
            'required_skills', 'responsibilities', 'application_method',
            'application_deadline', 'additional_notes'
        ]
        widgets = {
            'job_description': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 3}),
            'required_skills': forms.Textarea(attrs={'rows': 2}),
            'additional_notes': forms.Textarea(attrs={'rows': 2}),
        }