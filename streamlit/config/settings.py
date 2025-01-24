import os
from dotenv import load_dotenv

load_dotenv()

# FLASK_SERVER_PORT = os.environ.get('FLASK_SERVER_PORT', 5000)
# DEBUG = os.environ.get('DEBUG', False)

DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_DATABASE = os.environ['DB_DATABASE']

SFTP_HOST = os.environ['SFTP_HOST']
SFTP_USER = os.environ['SFTP_USER']
SFTP_PASS = os.environ['SFTP_PASS']
SFTP_PATH = os.environ['SFTP_PATH']

KEYCLOAK_URL = os.environ["KEYCLOAK_URL"].strip()
KEYCLOAK_REALM = os.environ["KEYCLOAK_REALM"].strip()
KEYCLOAK_CLIENT = os.environ["KEYCLOAK_CLIENT"].strip()

DEPLOYED_IN_TEST = os.getenv("DEPLOYED_IN_TEST", 'False').lower() in ('true', '1', 't')

# APPLIKATOR_USERNAME = os.environ['APPLIKATOR_USERNAME']
# APPLIKATOR_PASSWORD = os.environ['APPLIKATOR_PASSWORD']
# APPLIKATOR_TENANT = os.environ['APPLIKATOR_TENANT']
# APPLIKATOR_BASE_URL = 'https://portal-cloud.applikator.dk/api'

VITACOMM_API_KEY = os.environ['VITACOMM_API_KEY']
VITACOMM_URL = 'https://vitacomm.dk/api/portal/CallReport/GetCallReport'

SEED_FILE = 'config/seed.json'
