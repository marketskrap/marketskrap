from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import os
def landing_page(request):
    return render(request, 'index.html')
@login_required 
def marketing_dashboard(request): 
    return render(request, 'dashboard/dashboard.html')  

def get_suppress_list(request):
    return JsonResponse({"message": "Suppress list function is working!"})   
def file_processing(request):
    return JsonResponse({"message": "File Processing function is working!"})
def script_execution(request):
    return JsonResponse({"message": "Script executed"})