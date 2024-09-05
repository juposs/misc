#!/usr/bin/python3
import telebot
from bistro_class import BistroMenu

# create a new bot using @botfather and enter its token here
token = ""

bot = telebot.TeleBot(token)

c1 = telebot.types.BotCommand(command='mondaymenu', description='Menu for Monday')
c2 = telebot.types.BotCommand(command='tuesdaymenu', description='Menu for Tuesday')
c3 = telebot.types.BotCommand(command='wednesdaymenu', description='Menu for Wednesday')
c4 = telebot.types.BotCommand(command='thursdaymenu', description='Menu for Thursday')
c5 = telebot.types.BotCommand(command='fridaymenu', description='Menu for Friday')
bot.set_my_commands([c1,c2,c3,c4,c5])

# Startup message
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello at JpoTestBot, get the current lunch menu here uncomplicated and anytime. Simply use the menu to select a day and be disappointed right away! At the moment only the menu for the current week is supported.")

@bot.message_handler(commands=["mondaymenu", "tuesdaymenu", "wednesdaymenu", "thursdaymenu", "fridaymenu"])
def send_menu(message):
    # parse requested weekday out of the given command
    day = message.text.split("menu")[0][1:]
    for menu in BistroMenu().print_day(day):
        bot.send_message(message.chat.id, menu)


# default handler to handle all messages of the type "msg"
#@bot.message_handler(func=lambda msg: True)
#def echo_all(message):

bot.infinity_polling()
bot.set_chat_menu_button(message.chat.id, telebot.types.MenuButtonCommands('commands'))
