import datetime
from credsandservices.credsandservices import service


def insert_allday_event(message,bot):
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


def insert_timed_event(message,bot):
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