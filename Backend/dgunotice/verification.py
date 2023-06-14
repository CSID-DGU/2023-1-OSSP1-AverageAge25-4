import secrets
from pathlib import Path
import MySQLdb
from django.urls import reverse
import environ
import os


env = environ.Env(
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, ''),
    DATABASE_PORT=(str, ''),
    NAVER_ADDRESS=(str, ''),
    NAVER_ID=(str, ''),
    NAVER_PASSWORD=(str, ''),
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

def generate_token(length=15):
    token = secrets.token_urlsafe(length)
    return token

def verify_email_token(email, token, key):
    # Connect to MySQL
    conn = MySQLdb.connect(
        host=env('DATABASE_HOST'),
        user=env('DATABASE_USER'),
        passwd=env('DATABASE_PASSWORD'),
        db=env('DATABASE_NAME')
    )
    cursor = conn.cursor()

    # Retrieve the verify_temp_ids from the database
    cursor.execute("SELECT temp_id FROM Verify")
    verify_temp_ids = [row[0] for row in cursor.fetchall()]

    for verify_temp_id in verify_temp_ids:
        decrypted_email = key.decrypt(verify_temp_id)
        if email == decrypted_email:
            # Fetch the corresponding record from the database
            cursor.execute("SELECT token FROM Verify WHERE temp_id = %s", (verify_temp_id,))
            row = cursor.fetchone()
            if row is not None and row[0] == token:
                # Delete the record from the database
                cursor.execute("DELETE FROM Verify WHERE temp_id = %s", (verify_temp_id,))
                conn.commit()
                cursor.close()
                conn.close()
                return True

    cursor.close()
    conn.close()
    return False

def generate_verification_link(email, token):
    base_url = 'http://127.0.0.1:8000'
    try:
        url = reverse('verify_email')
    except Exception:
        url = '/verify/'
    link = f"{base_url}{url}?email={email}&token={token}"
    return link
