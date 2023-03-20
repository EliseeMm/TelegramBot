
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import telebot
import json
from constants import BOT_API_KEY,SCOPE
from weather import weather,selectedweather


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
SCOPES = SCOPE
service = service_builder()

@bot.message_handler(commands = ["help"])
def helplist(message):
    bot.send_message(message.chat.id,
    "/cal : view events appearing on users calendar.\n\n"
    "/weather : get the next 7 days weather for Durban\n"
    "or specify which city : weather <cityname>\n\n"
    "make an all day event:\nall_day <summary> <start date> <end date>\n\n"
    "make a timed event:\ntimed <summary> <startdate> <start time> <end date> <end time>\n\n"
    "delete calendar event:\ndel_event <event number>\n\n"
    "Formats:\n"
    "Dates : yyyy-mm-dd\n"
    "Time : hh:mm\n")

def help_needed(message):
    help = ["hello","hi","sup"]
    return message.text in help

@bot.message_handler(func = help_needed)
def greet(message):
    bot.reply_to(message, "Hey there,My Name is Aux, How can i /help you ?")


@bot.message_handler(commands = ["cal"])
def calendar(message):
    bot.send_message(message.chat.id,"Finding events")
    calen(message)


def calen(message):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    try:
        events = list_of_event(message)
        event_output(message,events)
    except HttpError as error:
        bot.reply_to('An error occurred: %s' % error)

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

def event_output(message,events):
    eventsdict = {}
    eventnum = 1
    if events:
        for event in events:
            
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            eventsdict[str(eventnum)] = [start,end,event['summary']]
            eventnum += 1

        response = ""

        for key,value in eventsdict.items():
            if len(value[0]) > 10:
                date = value[0][:10]
                time = f'{value[0][11:16]}-{value[1][11:16]}'
                responsestring = f"{key})    {date}  {time.rjust(15,' ')}  {value[2].rjust(10,' ')}\n"

            else:
                date = value[0]
                time = value[1]
                responsestring = f"{key})    {date}  {time.rjust(15,' ')}  {value[2].rjust(10,' ')}\n"
            response += responsestring

        bot.send_message(message.chat.id,f"avaialble events\n{response}")
 
    return eventsdict

def del_event(message):
    command_list = message.text.split()
    if command_list[0].lower() == "del_event" and command_list[1].isdigit():
        return True

@bot.message_handler(func=del_event)
def delete_event(message):
    events = list_of_event(message)
    num = int(message.text.split()[1])
    if events and num <= len(events):
        event_id = events[num - 1]["id"]
        service.events().delete(calendarId = "primary",eventId = event_id).execute()
        bot.send_message(message.chat.id,f"Event \"{events[num-1]['summary']}\" Deleted")
        events = list_of_event(message)
        event_output(message,events)
    elif num > len(events):
        bot.send_message(message.chat.id,"Invalid event selection")
    else:
        bot.send_message(message.chat.id,"No events left")


def validate_make_allday_event(message):
    commands_list = tuple(message.text.split())
    if len(commands_list) == 4:
        command = commands_list[0]
        if command == "all_day":
            return True

    
@bot.message_handler(func = validate_make_allday_event)
def make_allday_event(message):
    command = message.text.split()
    summary = command[1]
    startdate = command[2]
    enddate = command[3]
    try:
        datetime.date(year = int(startdate[:3]),month = int(startdate[5:7]),day = int(startdate[8:10]))
        datetime.date(year = int(enddate[:3]),month = int(enddate[5:7]),day = int(enddate[8:10]))
        event = {
            "summary": summary,
            "start" : {"date" : startdate},
            "end" : {"date" : enddate}
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        bot.send_message(message.chat.id,f"event: '{summary}' created.")
    except:
        bot.reply_to(message,"Invalid date/time entered")


def validate_make_timed_event(message):
    commands_list = tuple(message.text.split())
    
    if len(commands_list) == 5:
        command= commands_list[0]
        if command == "timed":
            return True
    

@bot.message_handler(func = validate_make_timed_event)
def make_timed_event(message):
    commands_list = message.text.split()
    command,summary,startdate,starttime,endtime = commands_list[0],commands_list[1],commands_list[2],commands_list[3],commands_list[4]  
    try:
        datetime.date(year = int(startdate[:3]),month = int(startdate[5:7]),day = int(startdate[8:10]))
        datetime.time(hour=int(starttime[0:2]),minute=int(starttime[3:5]))
        datetime.time(hour=int(endtime[0:2]),minute=int(endtime[3:5]))
        event = {
            "summary": summary,
            "start" : {
                "dateTime" : f"{startdate}T{starttime}:00+02:00",
                "timeZone": "Africa/Johannesburg"
                }, 
            "end" : {
                "dateTime" : f"{startdate}T{endtime}:00+02:00",
                "timeZone": "Africa/Johannesburg"
                }
        }
        event = service.events().insert(calendarId='primary', body=event).execute()

        bot.send_message(message.chat.id,f"event: '{summary}' created.")

    except ValueError as e:
        bot.reply_to(message,"Invalid date/time entered")


@bot.message_handler(commands = ["print"])
def show(message):
    print(message)

@bot.message_handler(commands = ["weather"])
def botweather(message):
    weather(message,bot)

def city_weather(message):
    commands = tuple(message.text.split())
    if len(commands) > 1:
        command,city = commands
        if command.lower() == "weather":
            return commands

@bot.message_handler(func = city_weather)
def show_weather(message):
    city = city_weather(message)[1]
    selectedweather(message,bot,city)

bot.polling()