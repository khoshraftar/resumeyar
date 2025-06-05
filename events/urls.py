from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('log/', views.log_request, name='log_request'),
] 