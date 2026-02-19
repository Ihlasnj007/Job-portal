from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import JobPost
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from accounts.models import JobSeekerProfile
from django.contrib import messages
from .forms import JobApplicationForm
from .models import ApplicationPage
import os
import mimetypes
from django.http import FileResponse,Http404
from django.db.models import Q

# Create your views here.

@login_required
def available_jobs(request):
    user = request.user
    if user.is_employer:
        return redirect('login')

    query = request.GET.get('q')
    selected_job_types = request.GET.getlist('job_type')
    selected_experience_levels = request.GET.getlist('experience_level')
    selected_date_posted = request.GET.getlist('date_posted')
    
    jobs = JobPost.objects.all()

    if user.is_jobseeker:
        try:
            jobseeker = JobSeekerProfile.objects.get(user=user)
            applied_job_ids = ApplicationPage.objects.filter(jobseeker=jobseeker).values_list('job_id', flat=True)
            jobs = jobs.exclude(id__in=applied_job_ids)
        except JobSeekerProfile.DoesNotExist:
            return redirect('login')

    if query:
        jobs=jobs.filter(job_title__icontains=query)

    if selected_job_types:
        jobs = jobs.filter(job_type__in = selected_job_types)

    if selected_experience_levels:
        jobs = jobs.filter(required_experience__in = selected_experience_levels)

    if selected_date_posted:
        now = timezone.now()
        date_filters = []

        for option in selected_date_posted:
            if option == "Last 24 hours":
                date_filters.append(now - timedelta(days=1))
            elif option == "Last week":
                date_filters.append(now - timedelta(weeks=1))
            elif option == "Last month":
                date_filters.append(now - timedelta(days=30))
        
        if date_filters:
            most_recent = max(date_filters)
            jobs = jobs.filter(created_at__gte=most_recent)

    job_type_options = ['Full Time', 'Part Time', 'Contract', 'Internship']
    experience_level_options = ['Entry Level', 'Mid Level', 'Senior Level', 'Executive']
    date_posted_options = ['Last 24 hours', 'Last week', 'Last month']

    paginator = Paginator(jobs, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': user,
        'jobs': page_obj,
        'query': query,
        'job_type_options':job_type_options,
        'experience_level_options': experience_level_options,
        'date_posted_options': date_posted_options,
        'selected_job_types': selected_job_types,
        'selected_experience_levels': selected_experience_levels,
        'selected_date_posted': selected_date_posted,
        'paginator': paginator,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'applications/available_jobs.html', context)

@login_required
def application_page(request, job_id):
    user = request.user
    if not user.is_jobseeker:
        return redirect('login')
    
    job = get_object_or_404(JobPost, id=job_id)
    jobseeker = JobSeekerProfile.objects.get(user=user)
   
    if request.method == 'POST':
        form = JobApplicationForm(request.POST) 
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.jobseeker = jobseeker
            application.resume = jobseeker.resume
            application.email = user.email
            application.phone_number = jobseeker.phone_number
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect('available_jobs')
    else:
        form = JobApplicationForm()
     
    context = {
        'form': form,
        'job': job,
        'jobseeker': jobseeker,
        'user': user,
    }

    return render(request, 'applications/application_page.html', context)

@login_required
def my_applications(request):
    user = request.user
    if not user.is_jobseeker:
        return redirect('login')
    
    jobseeker = JobSeekerProfile.objects.get(user=user)
    applications = ApplicationPage.objects.filter(jobseeker = jobseeker)

    selected_status = request.GET.get('status')
    if selected_status in ['Pending','Rejected','Shortlisted']:
        applications = applications.filter(status=selected_status)

    context = {
        'user': user,
        'applications': applications,
        'selected_status': selected_status,
    }

    return render(request, 'applications/my_applications.html', context)

@login_required
def employer_jobs(request):
    if not request.user.is_employer:
        return redirect('login')
    
    query = request.GET.get('q')
    jobs = JobPost.objects.filter(employer=request.user).order_by('-created_at')

    if query:
        jobs = jobs.filter(job_title__icontains=query)

    paginator = Paginator(jobs, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    context = {
        'jobs': page_obj,
        'query': query,
        'paginator': paginator,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'applications/employer_jobs.html', context)

@login_required
def employer_applicants(request, job_id):
    user = request.user
    if not user.is_employer:
        return redirect('login')
    
    job = get_object_or_404(JobPost, id=job_id, employer=user)
    applicants = ApplicationPage.objects.filter(job=job)

    # For Pending, Shortlisted, Rejected
    selected_status = request.GET.get('status')
    if selected_status in ['Pending','Shortlisted','Rejected']:
        applicants = applicants.filter(status=selected_status)

    context = {
        'user':user,
        'job': job,
        'applicants' : applicants,
        'selected_status' : selected_status,
    }

    return render(request, 'applications/employer_applicant_list.html', context)

@login_required
def view_resume(request, application_id):
    user = request.user
    if not user.is_employer:
        return redirect('login')
    
    application = get_object_or_404(ApplicationPage, id=application_id)

    resume_path = application.resume.path

    if os.path.exists(resume_path):

        #Detect file based on extension. (content_type, _ = means mimetypes return a tuple value, for unpacking we use ', _'.)
        content_type, _ = mimetypes.guess_type(resume_path)
        if content_type is None:
            content_type = 'application/octet-stream'

        return FileResponse(open(resume_path, 'rb'), content_type=content_type)
    else:
        raise Http404("Oops.. Resume File not Found...!")
    
@login_required
def update_application_status(request, application_id):
    user = request.user
    if not user.is_employer:
        return redirect('login')
    
    application = get_object_or_404(ApplicationPage, id=application_id)

    new_status = request.POST.get('new_status')
    if new_status in ['Shortlisted','Rejected']:
        application.status = new_status
        application.save()
        messages.success(request, f"Application is {new_status}.")
    else:
        messages.error(request, "Invalid Status..!")
    
    return redirect('employer_applicant_list', job_id=application.job.id) # We pass job_id because url of employerApplicant requires an id which is the job id.

def mark_mail_sent(request, applicant_id):
    applicant = get_object_or_404(ApplicationPage, id=applicant_id)

    if request.method=='POST' and request.user.is_employer:
        if applicant.status == 'Shortlisted' and not applicant.mail_sent:
            applicant.mail_sent = True
            applicant.save()

    return redirect(request.META.get('HTTP_REFERER', 'employer_dashboard'))

@login_required
def view_job(request, job_id):
    user= request.user
    if not user.is_jobseeker:
        return redirect('login')
    
    job = get_object_or_404(JobPost, id=job_id)

    return render(request, 'applications/jobseeker_view_job.html', {'job':job})

@login_required
def withdraw_application(request, application_id):
    user=request.user
    if not user.is_jobseeker:
        return redirect('login')
    
    application = get_object_or_404(ApplicationPage, id=application_id, jobseeker=request.user.jobseeker_profile)

    if request.method=="POST":
        application.delete()
        messages.success(request, 'Your Application Has been deleted Successfully...!')
        return redirect('my_applications')

@login_required 
def recommended_jobs(request):
    user = request.user
    if not user.is_jobseeker:
        return redirect('login')
    
    jobs = JobPost.objects.all()

    # Exclude jobs that jobseekers already applied
    if user.is_jobseeker:
        try:
            jobseeker = JobSeekerProfile.objects.get(user=user)
            applied_job_ids = ApplicationPage.objects.filter(jobseeker=jobseeker).values_list('job_id', flat=True)
            jobs = jobs.exclude(id__in=applied_job_ids)
        except JobSeekerProfile.DoesNotExist:
            return redirect('login')

    # Extract profession and skills
    profession = jobseeker.profession.lower()
    skills = [skill.strip().lower() for skill in jobseeker.skills.split(',') if skill.strip()]

    # Build skill-based Q object
    skill_queries = Q()
    for skill in skills:
        skill_queries |= Q(job_description__icontains=skill) | Q(job_title__icontains=skill)

    # Filter jobs based on profession or skill match
    recommended = jobs.filter(
        Q(job_title__icontains=profession) |
        Q(job_description__icontains=profession) |
        skill_queries
    ).distinct() #distinct to avoid duplicates while recommending

    paginator = Paginator(recommended, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recommended_jobs': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'applications/recommended_jobs.html', context)
