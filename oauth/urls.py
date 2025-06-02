from django.urls import path
from .views import OAuthLoginView, OAuthCallbackView

app_name = 'oauth'

urlpatterns = [
    path('login/', OAuthLoginView.as_view(), name='login'),
    path('login/redirect/', OAuthLoginView.as_view(), {'redirected': True}, name='login_redirect'),
    path('callback/', OAuthCallbackView.as_view(), name='callback'),
] 