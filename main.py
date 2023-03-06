
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import telebot
import json
from constants import BOT_API_KEY

def get_creds():
    """Creates and stores the login credentials"""

    creds = None
   
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


def service_builder():
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)

    return service


bot = telebot.TeleBot(BOT_API_KEY,parse_mode = None)
SCOPES = ['https://www.googleapis.com/auth/calendar']
service = service_builder()

@bot.message_handler(commands = ["hello"])
def greet(message):
    bot.reply_to(message, "Hey there,My Name is Aux, How can i help you ?")


@bot.message_handler(commands = ["cal"])
def calendar(message):
    bot.send_message(message.chat.id,"Finding events")
    calen(message)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def calen(message):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    try:
        list_of_event(message)

    except HttpError as error:
        print('An error occurred: %s' % error)

def list_of_event(message):
    # service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    events_json = json.dumps(events,indent = 4)
    with open("events_list.json", "w") as outfile:
        outfile.write(events_json)
    
    if not events:
        bot.reply_to(message,'No upcoming events found.')
        return


    eventsdict = {}
    eventnum = 1

    for event in events:
        
        start = event['start'].get('dateTime', event['start'].get('date'))
        eventsdict[str(eventnum)] = [start,event['summary']]
        eventnum += 1

    response = ""

    for key,value in eventsdict.items():

        responsestring = f"{key} {value[0]} {value[1]}\n"
        response += responsestring

    bot.send_message(message.chat.id,f"avaialble events\n{response}")
    return eventsdict


@bot.message_handler(commands= ["delevent"])
def delete_event(message):
    events = list_of_event(message)
    bot.send_message(message.chat.id,"Select event number to delete")

    


bot.polling()