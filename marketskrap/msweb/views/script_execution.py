import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

PYTHON_SCRIPTS_PATH = "/var/www/marketskrap.com/marketskrap/msweb/pyths/"

@csrf_exempt
def run_python_script(request):
    if request.method == 'POST':
        script_name = request.POST.get('script_name')  # e.g., "add_mail.py"
        file_path = request.POST.get('file_path')      # e.g., "/path/to/file.csv"

        if not script_name or not file_path:
            return JsonResponse({"success": False, "error": "Missing parameters."})

        script_full_path = os.path.join(PYTHON_SCRIPTS_PATH, script_name)

        if not os.path.exists(script_full_path):
            return JsonResponse({"success": False, "error": "Script not found."})

        try:
            result = subprocess.run(["python3", script_full_path, file_path], capture_output=True, text=True)
            return JsonResponse({"success": True, "output": result.stdout})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})
