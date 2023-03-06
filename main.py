
import telebot
from constants import BOT_API_KEY

bot = telebot.TeleBot(BOT_API_KEY,parse_mode = None)

@bot.message_handler(commands = ["hello"])
def greet(message):
    bot.reply_to(message, "Hey there,My Name is Aux, How can i help you ?")


bot.polling()