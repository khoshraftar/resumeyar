from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ResumeForm

def home(request):
    return render(request, 'resumeyar/home.html')

def about(request):
    return render(request, 'resumeyar/about.html')

@login_required
def dashboard(request):
    return render(request, 'resumeyar/dashboard.html')

@login_required
def my_resumes(request):
    # TODO: Add resume list logic
    return render(request, 'resumeyar/my_resumes.html')

@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('my_resumes')
    else:
        form = ResumeForm()
    return render(request, 'resumeyar/create_resume.html', {'form': form})

@login_required
def edit_resume(request, resume_id):
    # TODO: Add resume editing logic
    return render(request, 'resumeyar/edit_resume.html')

@login_required
def resume_templates(request):
    # TODO: Add templates list logic
    return render(request, 'resumeyar/templates.html')

@login_required
def settings(request):
    # TODO: Add settings logic
    return render(request, 'resumeyar/settings.html') 