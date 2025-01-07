from django.shortcuts import render

def landing_page(request):
    return render(request, 'index.html')
def admin_login(request):
    return render(request, '/jazzmin/templates/adminindex.html')