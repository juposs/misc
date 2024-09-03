#!/usr/bin/python3
import telebot

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
    bot.send_message(message.chat.id, "Hello at JpoTestBot, get the current lunch menu here uncomplicated and anytime. Just use the menu to selet the day you die to know the menu for and be disappointed right away! At the moment only the menu for the current week is supported.")

@bot.message_handler(commands=["mondaymenu", "tuesdaymenu", "wednesdaymenu", "thursdaymenu", "fridaymenu"])
def send_menu(message):
    # NOTE Paste code from bistro.py here
    if "monday" in message.text.lower():
        pass
    if "tuesday" in message.text.lower():
        pass
    if "wednesday" in message.text.lower():
        pass
    if "thursday" in message.text.lower():
        pass
    if "friday" in message.text.lower():
        pass
    bot.send_message(message.chat.id, f"comming soon.. to a town near you {message.text}")



# default handler to handle all messages of the type "msg"
#@bot.message_handler(func=lambda msg: True)
#def echo_all(message):

bot.infinity_polling()
bot.set_chat_menu_button(message.chat.id, telebot.types.MenuButtonCommands('commands'))
