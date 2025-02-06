import os
import sys
import django
import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Set up Django
sys.path.append('/var/www/marketskrap.com/marketskrap')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketskrap.settings')
django.setup()

db_settings = settings.DATABASES['default']
BASE_PATH = '/var/www/marketskrap.com/marketskrap/msweb/reposit'
EXPECTED_COLUMNS = ['email_ID','mobile_number', 'first_Name', 'last_Name', 'date_of_addition', 'source', 'email_status']

def validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if list(df.columns) == EXPECTED_COLUMNS:
            return df
        else:
            return None
    except Exception as e:
        return None

def convert_dates(df):
    try:
        df['date_of_addition'] = pd.to_datetime(df['date_of_addition'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
        return df
    except Exception as e:
        return df

def remove_duplicates(df):
    try:
        engine = create_engine(f"mysql+pymysql://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}/{db_settings['NAME']}")
        existing_emails_query = "SELECT email_ID FROM master_list"
        existing_emails_df = pd.read_sql(existing_emails_query, engine)
        
        total_uploaded = len(df)
        df = df[~df['email_ID'].isin(existing_emails_df['email_ID'])]
        total_added = len(df)
        total_duplicates = total_uploaded - total_added
        
        return df, total_uploaded, total_duplicates, total_added
    except SQLAlchemyError:
        return df, 0, 0, 0

def insert_data_to_db(df):
    try:
        engine = create_engine(f"mysql+pymysql://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}/{db_settings['NAME']}")
        df.to_sql('master_list', engine, if_exists='append', index=False)
    except SQLAlchemyError:
        pass

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not file_path or not os.path.isfile(file_path):
        print("0\n0\n0")
        sys.exit(1)

    df = validate_csv(file_path)
    if df is not None:
        df = convert_dates(df)
        df, total_uploaded, total_duplicates, total_added = remove_duplicates(df)
        
        if not df.empty:
            insert_data_to_db(df)

        print(total_uploaded)
        print(total_duplicates)
        print(total_added)
    else:
        print("0\n0\n0")
