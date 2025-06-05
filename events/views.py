from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.

def log_request(request):
    # Get request headers
    headers = dict(request.headers)
    
    # Get request body
    body = {}
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            body = {'raw_body': request.body.decode('utf-8', errors='ignore')}
    
    # Create response data
    response_data = {
        'method': request.method,
        'headers': headers,
        'body': body,
        'path': request.path,
        'query_params': dict(request.GET.items()),
    }
    
    # Print to console
    print("\n=== Request Details ===")
    print(f"Method: {request.method}")
    print("\nHeaders:")
    for key, value in headers.items():
        print(f"{key}: {value}")
    print("\nBody:")
    print(json.dumps(body, indent=2))
    print("\nQuery Parameters:")
    print(json.dumps(dict(request.GET.items()), indent=2))
    print("=====================\n")
    
    return HttpResponse(json.dumps(response_data, indent=2), content_type='application/json')
