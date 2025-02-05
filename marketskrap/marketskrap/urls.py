"""
URL configuration for marketskrap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfos.path.join(BASE_DIR, 'msweb/jet/dashboard/templates/admin'),
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static # Add this line
from .views import get_suppress_list
#from .views.file_processing import upload_file  # Import the function directly
#from .views.script_execution import run_python_script
from django.http import JsonResponse    

from msweb.views.file_processing import upload_file  # Corrected import
from msweb.views.script_execution import run_python_script  # Corrected import

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # Login page
    path('dashboard/', views.marketing_dashboard, name='marketing_dashboard'), # Marketing dashboard
    path('suppress_list/', get_suppress_list, name='get_suppress_list'),
    path('upload_file/', upload_file, name='upload_file'),  
    path('run_python_script/', run_python_script, name='run_python_script'),


   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


