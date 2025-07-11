from django.shortcuts import render,redirect,get_object_or_404
from .forms import JobPostForm
from .models import JobPost
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

def post_job(request):
    if not request.user.is_employer:
        return redirect('jobseeker_dashboard')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request,"Job Posted Successfully..!")
            return redirect('job_post')
    else:
        form = JobPostForm()

    return render(request, 'jobs/post_job.html', {'form':form})

@login_required
def employer_job_list(request):
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
    return render(request, 'jobs/employer_job_list.html', context)

@login_required
def edit_job(request,job_id):
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_job_list')
    else:
        form = JobPostForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'edit_mode': True})

@login_required
def delete_job(request, job_id):
    user = request.user
    if not user.is_employer:
        return redirect('login')
    
    job = get_object_or_404(JobPost, id=job_id, employer= request.user)

    job.delete()

    return redirect('employer_job_list')
