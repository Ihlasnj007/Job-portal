from django import forms
from .models import ApplicationPage

class JobApplicationForm(forms.ModelForm):
    cover_letter = forms.CharField(
        label="Cover Letter",
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write a message to the employer...'}),
        required=False
    )

    class Meta:
        model = ApplicationPage
        fields = ['cover_letter']