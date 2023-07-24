import datetime
from credsandservices.credsandservices import service
from googleapiclient.errors import HttpError
import json

def event_output(events):
    eventsdict = {}
    eventnum = 1
    
    if len(events) > 0:
        for event in events:
            
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            eventsdict[str(eventnum)] = [start,end,event['summary']]
            eventnum += 1

        response = f"available events\n"

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
        
    else:
        response = "No available events"
    return response
    
def calen(message,bot):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    try:
        events = list_of_event()
        return event_output(events)

    except HttpError as error:
        bot.reply_to(message.chat.id,'An error occurred: %s' % error)
    
    

def list_of_event():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    events_json = json.dumps(events,indent = 4)
    with open("events_list.json", "w") as outfile:
        outfile.write(events_json)
    
    return events