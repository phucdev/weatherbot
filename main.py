#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Weather Bot to reply to Telegram messages
"""
Author: Phuc Tran Truong, Marcus Ding
Date: 19.07.2016

Large parts of the code are taken from the Conversationbot example (see 'python-telegram-bot' module).
https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py

This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import weather
import extractor
import time

# Alternative mit Reply Keyboard
from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# states of the conversation
START, REPLY, NEXT_QUEST, LOC_UNKNOWN, TIME_UNKNOWN, LOC_TIME_UNKNOWN = range(6)

TOKEN = "219296013:AAHENQyYMoWHSGs5bjPhhxHR2ai4uEHGQ7c" # token for telegram bot


def start(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Hi! Ich bin dein Wetterbot 🌞 Was willst du wissen?  '
                         'Antworte mit /cancel um die Unterhaltung zu beenden 😉\n\n',)

    return REPLY

# Alternative mit Reply Keyboard
"""
def start(bot, update):
    reply_keyboard = [['Wetter jetzt in Berlin', 'Temperatur jetzt in Berlin', '/cancel']]
    bot.sendMessage(update.message.chat_id,
                    text='Hi! Ich bin dein Wetterbot 🌞 Was willst du wissen?  '
                         'Antworte mit /cancel um die Unterhaltung zu beenden 😉\n\n',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return REPLY
"""

def reply(bot, update):
    extr_request = extractor.get_args(update.message.text)
    code, reply = extractor.unknown_reply(extr_request)
    if (code == 0):
        bot.sendMessage(update.message.chat_id,text=reply)
        return REPLY
    elif (code == 2):
        bot.sendMessage(update.message.chat_id,text=reply)
        return LOC_UNKNOWN

    bot.sendMessage(update.message.chat_id,text="Ich schaue mal nach 😊" + reply)

    bot.sendMessage(update.message.chat_id,text=weather.deliver(*extr_request))
    time.sleep(3)
    bot.sendMessage(update.message.chat_id, text='Kann ich dir sonst noch helfen? 🙄')
    return REPLY

"""
def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    bot.sendMessage(update.message.chat_id,
                    text='Thank you! I hope we can talk again some day.')

    return ConversationHandler.END
"""

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='Ok bis bald!')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            REPLY: [MessageHandler([Filters.text], reply)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
