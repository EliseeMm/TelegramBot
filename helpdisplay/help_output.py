def output_help():
    """
    The output_help function returns a string containing the help text for the bot.
    It is called when a user sends /help to the bot.
    
    :return: A string with all of the accepted commands and their usage
    """
    return ("/help : displays how to use accepted commands\n\n"
    "/calendar : view current and future events appearing on users calendar.\n\n"
    "/weather : get the next 7 days weather for Durban\n"
    "or specify which city : weather <cityname>\n\n"
    "/loadshedding : return loadshedding times for\n"
    "specified areas\n\n"
    "send email: email, address, subject, mail content\n\n"
    "make an all day event:\nall_day <summary> <start date> <end date>\n\n"
    "make a timed event:\ntimed <summary> <startdate> <start time> <end date> <end time>\n\n"
    "delete calendar event:\ndel_event <event number>\n\n"
    "Formats:\n"
    "Dates : yyyy-mm-dd\n"
    "Time : hh:mm\n")