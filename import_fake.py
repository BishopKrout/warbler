import csv
import psycopg2

# Define the column headers
USERS_CSV_HEADERS = ['email', 'username', 'image_url', 'password', 'bio', 'header_image_url', 'location']
MESSAGES_CSV_HEADERS = ['text', 'timestamp', 'user_id']
FOLLOWS_CSV_HEADERS = ['user_being_followed_id', 'user_following_id']

# Database connection parameters
db_params = {
    'dbname': 'warbler',
    'user': 'bishop',
    'password': '2255',
    'host': 'localhost',
}

def import_data(file_path, table_name, columns):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip the header row
                for row in reader:
                    cur.execute(
                        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})",
                        row
                    )

# Import users
import_data('generator/users.csv', 'users', USERS_CSV_HEADERS)

# Import messages
import_data('generator/messages.csv', 'messages', MESSAGES_CSV_HEADERS)

# Import follows
import_data('generator/follows.csv', 'follows', FOLLOWS_CSV_HEADERS)
