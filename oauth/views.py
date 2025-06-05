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
        # Show the loading page first
        return render(request, 'oauth/redirect.html')

class OAuthRedirectView(View):
    def get(self, request):
        # Prepare OAuth parameters
        params = {
            'client_id': settings.OAUTH_CLIENT_ID,
            'redirect_uri': settings.OAUTH_REDIRECT_URI,
            'response_type': 'code',
            'scope': settings.OAUTH_SCOPE,
            'state': 'random_state_string'  # You should generate and validate this
        }
        # Redirect to Divar's authorization page
        auth_url = f"{settings.OAUTH_AUTHORIZATION_URL}?{urlencode(params)}"
        return redirect(auth_url)

class OAuthCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        
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
            headers = {
                'X-API-Key': settings.API_KEY
            }
            response = requests.post(settings.OAUTH_TOKEN_URL, data=token_data, headers=headers)
            response.raise_for_status()
            token_info = response.json()

            # Store tokens in session
            request.session['access_token'] = token_info.get('access_token')
            request.session['refresh_token'] = token_info.get('refresh_token')
            
            # Get user profile using the access token
            headers = {'Authorization': f'Bearer {token_info["access_token"]}'}
            print(headers)
            
            # Store user profile in session            
            return redirect('home')  # Redirect to your home page or dashboard
            
        except requests.exceptions.RequestException as e:
            return HttpResponse(f'Error in OAuth flow: {str(e)}', status=400)
