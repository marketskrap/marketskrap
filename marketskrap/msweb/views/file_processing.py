import os
import datetime
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

UPLOAD_DIR = "/var/www/marketskrap.com/marketskrap/msweb/reposit"

# ✅ Ensure the database connection
db_settings = settings.DATABASES['default']
engine = create_engine(f"mysql+pymysql://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}/{db_settings['NAME']}")

EXPECTED_COLUMNS = ['email_ID', 'mobile_number', 'first_Name', 'last_Name', 'date_of_addition', 'source', 'email_status']

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # ✅ Accept only CSV files
        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({"success": False, "error": "Only CSV files are allowed."})

        # ✅ Generate timestamp-based filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.csv"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        try:
            # ✅ Ensure the directory exists
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            # ✅ Save the uploaded file
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # ✅ Process the CSV file in Django (no need for add_mail.py)
            return process_csv(file_path)

        except Exception as e:
            return JsonResponse({"success": False, "error": f"File save error: {str(e)}"})

    return JsonResponse({"success": False, "error": "No file uploaded."})

def process_csv(file_path):
    try:
        df = pd.read_csv(file_path)

        # ✅ Validate columns
        if list(df.columns) != EXPECTED_COLUMNS:
            return JsonResponse({"success": False, "error": "Invalid CSV format."})

        # ✅ Convert date formats
        df['date_of_addition'] = pd.to_datetime(df['date_of_addition'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')

        # ✅ Check for duplicates
        existing_emails_query = "SELECT email_ID FROM master_list"
        existing_emails_df = pd.read_sql(existing_emails_query, engine)

        total_uploaded = len(df)
        df = df[~df['email_ID'].isin(existing_emails_df['email_ID'])]
        total_added = len(df)
        total_duplicates = total_uploaded - total_added

        # ✅ Insert new records into the database
        if not df.empty:
            df.to_sql('master_list', engine, if_exists='append', index=False)

        return JsonResponse({
            "success": True,
            "file_path": file_path,
            "total_uploaded": total_uploaded,
            "total_duplicates": total_duplicates,
            "total_added": total_added
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": f"CSV Processing Error: {str(e)}"})
