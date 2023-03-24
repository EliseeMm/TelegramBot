from credsandservices.credsandservices import service
from eventresources.calendar_resources import list_of_event,event_output


def delete_events(message,bot):
    events = list_of_event(message,bot)
    
    num = int(message.text.split()[1])
    if not events: 
        bot.send_message(message.chat.id,"No events to delete")
    elif events and 0 <num <= len(events):
        event_id = events[num - 1]["id"]
        service.events().delete(calendarId = "primary",eventId = event_id).execute()
        bot.send_message(message.chat.id,f"Event \"{events[num-1]['summary']}\" Deleted")
        events = list_of_event(message,bot)
        event_output(message,events,bot)
    elif num > len(events) or num == 0:
        bot.send_message(message.chat.id,"Invalid event selection")


    

