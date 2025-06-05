from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ResumeForm
from .models import Resume

@login_required(login_url='oauth:login')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='oauth:login')
def my_resumes(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'dashboard/my_resumes.html', {'resumes': resumes})

@login_required(login_url='oauth:login')
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('dashboard:my_resumes')
    else:
        form = ResumeForm()
    return render(request, 'dashboard/create_resume.html', {'form': form})

@login_required(login_url='oauth:login')
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('dashboard:my_resumes')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'dashboard/edit_resume.html', {'form': form, 'resume': resume})

@login_required(login_url='oauth:login')
def resume_templates(request):
    return render(request, 'dashboard/templates.html')

@login_required(login_url='oauth:login')
def settings(request):
    return render(request, 'dashboard/settings.html')
