# accounts/views.py
from django.shortcuts import render, redirect
from .forms import JobSeekerRegistrationForm,EmployerRegistrationForm,EmailLoginForm, JobSeekerProfileForm
from .models import JobSeekerProfile,EmployerProfile
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from jobs.models import JobPost
from applications.models import ApplicationPage

def Jobseeker_Register(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_jobseeker = True
            user.save()

            JobSeekerProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number'),
                profession=form.cleaned_data.get('profession'),
                experience=form.cleaned_data.get('experience'),
                education=form.cleaned_data.get('education'),
                skills=form.cleaned_data.get('skills'),
                resume=form.cleaned_data.get('resume'),
                cover_letter=form.cleaned_data.get('cover_letter'),
            )

            return redirect('login')
    else:
        form = JobSeekerRegistrationForm()
    
    return render(request, 'accounts/Jobseeker_register.html', {'form': form})

def Employer_Register(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_employer = True
            user.save()

            EmployerProfile.objects.create(
                user=user,
                company_name=form.cleaned_data.get('company_name'),
                company_website=form.cleaned_data.get('company_website'),
                company_location=form.cleaned_data.get('company_location'),
                contact_number=form.cleaned_data.get('contact_number'),
                company_description=form.cleaned_data.get('company_description'),
            )

            return redirect('login')
    else:
        form = EmployerRegistrationForm()

    return render(request, 'accounts/employer_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                if user.is_employer:
                    return redirect('employer_dashboard')
                elif user.is_jobseeker:
                    return redirect('jobseeker_dashboard')
            else:
                form.add_error(None, 'Invalid Username or Password!')
    else:
        form = EmailLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def employer_dashboard(request):
    user = request.user
    if not user.is_employer:
        return redirect('login')
    
    total_jobs = JobPost.objects.filter(employer=user).count()
    jobs_posted = JobPost.objects.filter(employer=user)
    total_applicants = ApplicationPage.objects.filter(job__in=jobs_posted).count()
    total_shortlisted = ApplicationPage.objects.filter(job__in = jobs_posted, status='Shortlisted').count()
    company_name = request.user.employer_profile.company_name

    context = {
        'user': user,
        'total_jobs': total_jobs,
        'company_name': company_name,
        'total_applicants': total_applicants,
        'total_shortlisted':total_shortlisted,
    }
    return render(request, 'accounts/employer_dashboard.html', context)


@login_required
def jobseeker_dashboard(request):
    user = request.user
    if not user.is_jobseeker:
        return redirect('login')
    try:
        profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        profile = None
        
    return render(request, 'accounts/jobseeker_dashboard.html', {'profile': profile})


@login_required
def my_profile(request):
    if not request.user.is_jobseeker:
        return redirect('login')
    
    profile = JobSeekerProfile.objects.get(user=request.user)
    return render(request, 'accounts/my_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    if not request.user.is_jobseeker:
        return redirect('login')
    
    profile = JobSeekerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = JobSeekerProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile':profile,
    })
