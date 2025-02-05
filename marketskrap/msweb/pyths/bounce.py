# bounce.py
import os
import sys
import django
from django.conf import settings
from prettytable import PrettyTable
import pymysql

sys.path.append('/var/www/marketskrap.com/marketskrap')  # Path to your project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketskrap.settings')

django.setup()

db_settings = settings.DATABASES['default']

connection = pymysql.connect(
    host=db_settings['HOST'],
    user=db_settings['USER'],
    password=db_settings['PASSWORD'],
    database=db_settings['NAME']
)

query = "SELECT * FROM marketskrap_db.bounce_tbl"
cursor = connection.cursor()
cursor.execute(query)
columns = [desc[0] for desc in cursor.description]
rows = cursor.fetchall()
cursor.close()
connection.close()

def generate_table_html(page, rows_per_page=10):
    table = PrettyTable()
    table.field_names = columns

    start = (page - 1) * rows_per_page
    end = start + rows_per_page
    for row in rows[start:end]:
        table.add_row(row)

    table_html = table.get_html_string()

    pagination_html = f"""
    <div class='pagination'>
        <button onclick="fetchSuppressList({page - 1})" {'disabled' if page <= 1 else ''}>Previous</button>
        <button onclick="fetchSuppressList({page + 1})" {'disabled' if end >= len(rows) else ''}>Next</button>
    </div>
    """
    
    return table_html + pagination_html

if __name__ == "__main__":
    page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    html_content = generate_table_html(page)
    with open('/var/www/marketskrap.com/marketskrap/msweb/pyths/table_output.html', 'w') as file:
        file.write(html_content)
    print(html_content)
