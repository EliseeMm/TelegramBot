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
    bot.send_message(message.chat.id,output_help())

def help_needed(message):
    help = ["hello","hi","sup"]
    return message.text in help

@bot.message_handler(func = help_needed)
def greet(message):
    bot.reply_to(message, "Hey there,My Name is Aux, How can i /help you ?")

@bot.message_handler(commands = ["calendar"])
def calendar(message):
    bot.send_message(message.chat.id,"Finding events")
    response = calen(message,bot)
    bot.send_message(message.chat.id,response)


def del_event(message):
    command_list = message.text.split()
    if command_list[0].lower() == "del_event" and command_list[1].isdigit():
        return True

@bot.message_handler(func=del_event)
def deleteevent(message):
    response = delete_events(message,bot)
    bot.send_message(message.chat.id, response)


def validate_make_allday_event(message):
    commands_list = tuple(message.text.split())
    if len(commands_list) == 4:
        command = commands_list[0]
        if command == "all_day":
            return True
  
@bot.message_handler(func = validate_make_allday_event)
def make_allday_event(message):
    response = insert_allday_event(message)
    bot.send_message(message.chat.id,response)


def validate_make_timed_event(message):
    commands_list = tuple(message.text.split())
    
    if len(commands_list) == 5:
        command= commands_list[0]
        if command == "timed":
            return True
    
@bot.message_handler(func = validate_make_timed_event)
def make_timed_event(message):
    response = insert_timed_event(message)
    bot.send_message(message.chat.id,response)

@bot.message_handler(commands = ["weather"])
def botweather(message):
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
    city = city_weather(message)[1]
    bot.reply_to(message,f"Getting the next 7 days weather for {city}")
    response = selectedweather(message,bot,city)
    bot.send_message(message.chat.id,response)


def validate_email(message):
    commands = tuple(message.text.split(","))
    command= commands[0]
    if command.lower() == "email":
        return True

@bot.message_handler(func = validate_email)
def send_email(message):
    commands = tuple(message.text.split(","))
    command,to,subject,mail, = commands
    gmail_send_message(to,subject,mail)
    bot.send_message(message.chat.id,f"Email '{subject}' sent to {to}.")

@bot.message_handler(commands = ["loadshedding"])
def loadshedding(message):
    response_loadshedding(message,bot)
    

bot.polling()