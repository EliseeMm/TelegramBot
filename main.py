import telebot
from constants import BOT_API_KEY
from weatherresources.weather import weather,selectedweather
from emailresources.emailing import gmail_send_message
from loadsheddingresources.loadshedding import response_loadshedding
from eventresources.calendar_resources import calen
from eventresources.delete_events import delete_events
from eventresources.create_events import insert_allday_event,insert_timed_event
from helpdisplay.help_output import output_help

bot = telebot.TeleBot(BOT_API_KEY,parse_mode = None)

@bot.message_handler(commands = ["help"])
def helplist(message):
    """
    The helplist function is a simple function that sends the user a list of commands available to them.
        It takes in one argument, message, which is the message sent by the user.
    
    :param message: Get the message from the user
    :return: The output_help function
    """
    bot.send_message(message.chat.id,output_help())

def help_needed(message):
    """
    The help_needed function checks if the message text is in a list of help messages.
    :param message: Get the text of the message
    :return: True if the message contains one of the words in help
    """
    help = ["hello","hi","sup"]
    return message.text in help

@bot.message_handler(func = help_needed)
def greet(message):
    """
    The greet function responds to a user that inputs 'hello'
    
    :param message: Get the message sent by the user
    :return: A message
    """
    bot.reply_to(message, "Hey there,My Name is Aux, How can i /help you ?")

@bot.message_handler(commands = ["calendar"])
def calendar(message):
    """
    The calendar function takes in a message and returns the next event on the calendar
    
    :param message: Get the message sent by the user
    :return: A string of events
    """
    bot.send_message(message.chat.id,"Finding events")
    response = calen(message,bot)
    bot.send_message(message.chat.id,response)


def del_event(message):
    """
    The del_event function takes a message object as input and returns True if the message text is of the form:
    del_event number; where number is an integer. Otherwise, it returns False.
    
    :param message: Get the message text from the user
    :return: True if the command is correct
    """
    command_list = message.text.split()
    if command_list[0].lower() == "del_event" and command_list[1].isdigit():
        return True

@bot.message_handler(func=del_event)
def deleteevent(message):
    """
    The deleteevent function deletes an event from the database.
        It takes in a message object and returns a string response to the user.
    
    :param message: Identify the event to be deleted
    :return: A string
    """
    response = delete_events(message,bot)
    bot.send_message(message.chat.id, response)


def validate_make_allday_event(message):
    """
    The validate_make_allday_event function checks if the user's input is valid.
        It takes in a message object and returns True or False depending on whether the command is valid.
    
    :param message: Get the user's input
    :return: True if the user enters a valid command
    """
    commands_list = tuple(message.text.split())
    if len(commands_list) == 4:
        command = commands_list[0]
        if command == "all_day":
            return True
  
@bot.message_handler(func = validate_make_allday_event)
def make_allday_event(message):
    """
    The make_allday_event function takes a message object as an argument and returns the response from the insert_allday_event function.
    The make_allday_event function also sends a message to the user with that response.
    
    :param message: Get the chat id of the user who sent the message
    :return: A message to the user
    """
    response = insert_allday_event(message)
    bot.send_message(message.chat.id,response)


def validate_make_timed_event(message):
    """
    The validate_make_timed_event function checks if the user's message is a valid timed event.
        It returns True if it is, and False otherwise.
    
    :param message: Get the text from the message sent by the user
    """
    commands_list = tuple(message.text.split())
    
    if len(commands_list) == 5:
        command= commands_list[0]
        if command == "timed":
            return True
    
@bot.message_handler(func = validate_make_timed_event)
def make_timed_event(message):
    """
    The make_timed_event function takes a message object as an argument and calls the insert_timed_event function,
    which returns a string. The make_timed_event function then sends that string to the user who sent the original message.
    
    :param message: Get the chat id of the user
    :return: The message that the user sent
    """
    response = insert_timed_event(message)
    bot.send_message(message.chat.id,response)

@bot.message_handler(commands = ["weather"])
def botweather(message):
    """
    The botweather function is a simple function that calls the weather() function
        and returns the response to the user. The botweather() function is called when 
        a user types /botweather in their chat with @DurbanWeatherBot
    
    :param message: Get the message from the user
    :return: A string with the weather forecast
    """
    bot.reply_to(message,"Getting the next 7 days weather for Durban")
    response = weather()
    bot.send_message(message.chat.id,response)


def city_weather(message):
    commands = tuple(message.text.split(" ",1))
    if len(commands) > 1:
        command,city = commands
        if command.lower() == "weather":
            return commands

@bot.message_handler(func = city_weather)
def show_weather(message):
    """
    The show_weather function takes a message object as an argument and returns the next 7 days weather for the city specified in the message.
        The function first calls on another function called city_weather to get a tuple containing both the user's id and their selected city.
        It then uses that information to call on another function called selectedweather which returns a string containing all of our desired weather data.
    
    :param message: Get the message sent by the user
    :return: The response from the selectedweather function
    """
    city = city_weather(message)[1]
    bot.reply_to(message,f"Getting the next 7 days weather for {city}")
    response = selectedweather(message,bot,city)
    bot.send_message(message.chat.id,response)


def validate_email(message):
    """
    The validate_email function checks if the user has entered a valid email address.
        If so, it returns True and sends an email to the user with their password.
        Otherwise, it returns False.
    
    :param message: Get the message that was sent to the bot
    :return: True if the command is email
    """
    commands = tuple(message.text.split(","))
    command= commands[0]
    if command.lower() == "email":
        return True

@bot.message_handler(func = validate_email)
def send_email(message):
    """
    The send_email function takes a message object as an argument.
    It then splits the text of the message into a tuple, and assigns each element to its own variable.
    The function then calls gmail_send_message with those variables as arguments, and sends a confirmation message to the user.
    
    :param message: Get the message sent by the user
    :return: The bot
    """
    commands = tuple(message.text.split(","))
    command,to,subject,mail, = commands
    gmail_send_message(to,subject,mail)
    bot.send_message(message.chat.id,f"Email '{subject}' sent to {to}.")

@bot.message_handler(commands = ["loadshedding"])
def loadshedding(message):
    """
    The loadshedding function is a function that takes in a message and returns the loadshedding schedule for the day.
        It uses the loadshedding_schedule() function to get today's schedule, then it sends back an image of today's 
        load shedding schedule.
    
    :param message: Get the message that is sent to the bot
    :return: A string
    """
    response_loadshedding(message,bot)
    

bot.polling()