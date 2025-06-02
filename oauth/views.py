from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.http import HttpResponse
import requests
import json
from urllib.parse import urlencode

# Create your views here.

class OAuthLoginView(View):
    def get(self, request):
        # If it's a direct access, show the redirect page
        if not request.GET.get('redirected'):
            return render(request, 'oauth/redirect.html')
            
        # If it's from the redirect page, proceed with OAuth
        params = {
            'client_id': settings.OAUTH_CLIENT_ID,
            'redirect_uri': settings.OAUTH_REDIRECT_URI,
            'response_type': 'code',
            'scope': settings.OAUTH_SCOPE,
        }
        auth_url = f"{settings.OAUTH_AUTHORIZATION_URL}?{urlencode(params)}"
        return redirect(auth_url)

class OAuthCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return HttpResponse('Authorization code not received', status=400)

        # Exchange code for access token
        token_data = {
            'client_id': settings.OAUTH_CLIENT_ID,
            'client_secret': settings.OAUTH_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.OAUTH_REDIRECT_URI,
        }

        try:
            response = requests.post(settings.OAUTH_TOKEN_URL, data=token_data)
            response.raise_for_status()
            token_info = response.json()

            # Store tokens in session
            request.session['access_token'] = token_info.get('access_token')
            request.session['refresh_token'] = token_info.get('refresh_token')
            
            return redirect('home')  # Redirect to your home page or dashboard
        except requests.exceptions.RequestException as e:
            return HttpResponse(f'Error exchanging code for token: {str(e)}', status=400)
