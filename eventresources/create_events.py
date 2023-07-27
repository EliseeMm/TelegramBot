import datetime
from credsandservices.credsandservices import service


def insert_allday_event(message):
    """
    The insert_allday_event function takes in a message object and returns a string.
    The function parses the text of the message to extract information about an event, 
    and then inserts that event into Google Calendar.
    
    :param message: Get the message sent by the user
    :return: A string
    """
    command = message.text.split()
    summary = command[1]
    startdate = command[2]
    enddate = command[3]
    response = ""
    try:
        datetime.date(year = int(startdate[:3]),month = int(startdate[5:7]),day = int(startdate[8:10]))
        datetime.date(year = int(enddate[:3]),month = int(enddate[5:7]),day = int(enddate[8:10]))
        event = {
            "summary": summary,
            "start" : {"date" : startdate},
            "end" : {"date" : enddate}
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        response += f"event: '{summary}' created."
    except:
        response += "Invalid date/time entered"

    return response


def insert_timed_event(message):
    """
    The insert_timed_event function takes in a message object and returns a string.
    The function splits the text of the message into 5 parts: command, summary, startdate, starttime and endtime.
    It then checks if these values are valid by using datetime's date() and time() functions to check if they are valid dates/times. 
    If they are not it will return an error response saying that invalid date/time was entered. If all is well it will create an event dictionary with the given values as keys for each value in their respective fields (summary,startdate etc). It then uses Google's API to insert this event
    
    :param message: Get the message sent by the user
    :return: A string
    """
    commands_list = message.text.split()
    command,summary,startdate,starttime,endtime = commands_list[0],commands_list[1],commands_list[2],commands_list[3],commands_list[4]
    response = ""
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
        response += f"event: '{summary}' created."
        return response


    except ValueError as e:
        response += "Invalid date/time entered"
    
    return response