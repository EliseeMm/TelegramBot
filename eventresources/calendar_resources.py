import datetime
from credsandservices.credsandservices import service
from googleapiclient.errors import HttpError
import json

def event_output(events):
    """
    The event_output function takes a list of events and returns a string with the following format:
        available events
        1)     2020-01-01  00:00 - 23:59   event name
        2)     2020-02-02  00:00 - 23:59   event name2
    
    :param events: Pass the events list to the function
    :return: A string with a list of events

    """
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
    """
    The calen function returns a list of events on the user's calendar.
        
    
    :param message: Pass the message from the user to the bot
    :param bot: Access the bot object and send messages back to the user
    :return: A list of events which are in the calendar
    """
    

    try:
        events = list_of_event()
        return event_output(events)

    except HttpError as error:
        bot.reply_to(message.chat.id,'An error occurred: %s' % error)
    
    

def list_of_event():
    """
    The list_of_event function will return a list of events on the user's calendar.
        The function takes no arguments and returns a list of dictionaries, each dictionary representing an event.
    
    :return: A list of events
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    events_json = json.dumps(events,indent = 4)
    with open("events_list.json", "w") as outfile:
        outfile.write(events_json)
    
    return events