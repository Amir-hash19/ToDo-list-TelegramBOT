import telebot
from database.base import engine, Base


Base.metadata.create_all(bind=True)

bot = telebot.TeleBot("Token")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello and Welcome to The Task Manager telegram Bot")