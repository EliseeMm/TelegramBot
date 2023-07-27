from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from constants import SCOPE
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
SCOPES = SCOPE


def get_creds():
    """Creates and stores the login credentials"""

    creds = None
   
    if os.path.exists('calendar_token.json'):
        creds = Credentials.from_authorized_user_file('calendar_token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('calendar_token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


def service_builder():
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)

    return service


service = service_builder()