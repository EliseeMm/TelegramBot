from credsandservices.credsandservices import service
from eventresources.calendar_resources import list_of_event,event_output


def delete_events(message,bot):
    events = list_of_event()
    
    num = int(message.text.split()[1])
    response  = ""
    
    if not events: 
        response += "No events to delete"

    elif events and 0 <num <= len(events):
        event_id = events[num - 1]["id"]
        service.events().delete(calendarId = "primary",eventId = event_id).execute()
        response += f"Event \"{events[num-1]['summary']}\" Deleted"
        events = list_of_event()
        event_output(events)

    elif num > len(events) or num == 0:
        response += "Invalid event selection"

    return response


    

