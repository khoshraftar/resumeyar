from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('resumes/', views.my_resumes, name='my_resumes'),
    path('resumes/create/', views.create_resume, name='create_resume'),
    path('resumes/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    path('templates/', views.resume_templates, name='resume_templates'),
    path('settings/', views.settings, name='settings'),
] 