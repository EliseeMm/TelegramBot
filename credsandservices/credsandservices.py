from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from constants import SCOPE
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
SCOPES = SCOPE


def get_creds():
    """
    The get_creds function creates and stores the login credentials.
        If there is a token file, it will use that to create the credentials.
        Otherwise, it will prompt you for your username and password.
    
    :return: An object of type credentials
    """

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
    """
    The service_builder function is used to build a service object that can be used to make requests
    to the Google Calendar API. The function uses the get_creds() function, which returns credentials 
    that are then passed into the build() method of googleapiclient.discovery.build(). This method returns 
    a service object that can be used to make requests.
    
    :return: A service object
    """
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)

    return service


service = service_builder()