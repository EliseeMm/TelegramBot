
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
        events = list_of_event(message)
        event_output(message,events)
    except HttpError as error:
        print('An error occurred: %s' % error)

def list_of_event(message):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    events_json = json.dumps(events,indent = 4)
    with open("events_list.json", "w") as outfile:
        outfile.write(events_json)
    
    if not events:
        bot.send_message(message.chat.id,'No upcoming events found.')
        return

    return events

# separate here return events

def event_output(message,events):
    eventsdict = {}
    eventnum = 1
    if events:
        for event in events:
            
            start = event['start'].get('dateTime', event['start'].get('date'))
            eventsdict[str(eventnum)] = [start,event['summary']]
            eventnum += 1

        response = ""

        for key,value in eventsdict.items():

            responsestring = f"{key} {value[0]} {value[1]}\n"
            response += responsestring

        bot.send_message(message.chat.id,f"avaialble events\n{response}")
        print(events)
    return eventsdict

def del_event(message):
    command_list = message.text.split()
    if command_list[0].lower() == "del_event" and command_list[1].isdigit():
        return True

@bot.message_handler(func=del_event)
def delete_event(message):
    events = list_of_event(message)
    print(events)
    num = int(message.text.split()[1])
    if events:
        event_id = events[num - 1]["id"]
        service.events().delete(calendarId = "primary",eventId = event_id).execute()
        bot.send_message(message.chat.id,"Event Deleted")
        events = list_of_event(message)
        event_output(message,events)
    else:
        bot.send_message(message.chat.id,"No events left")


def validate_make_event(message):
    commands_list = tuple(message.text.split())
    if len(commands_list) >= 3:
        command,date,description = commands_list[0],commands_list[1],commands_list[2]
        if command == "create_event" and description :
            return True
    
@bot.message_handler(func = validate_make_event)
def make_event(message):
    command = message.text.split()
    print(command)
    summary = command[1]
    startdate = command[2]
    enddate = command[3]
    event = {
        "summary": summary,
        "start" : {"date" : startdate},
        "end" : {"date" : enddate}
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    bot.send_message(message.chat.id,f"event: '{summary}' created.")


@bot.message_handler(commands = ["print"])
def show(message):
    print(message)

bot.polling()