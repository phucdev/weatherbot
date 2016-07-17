#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import weather
import extractor

from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

START, REPLY, NEXT_QUEST, LOC_UNKNOWN, TIME_UNKNOWN, LOC_TIME_UNKNOWN = range(6)

TOKEN = "219296013:AAHENQyYMoWHSGs5bjPhhxHR2ai4uEHGQ7c" # token for telegram bot


def start(bot, update):

    bot.sendMessage(update.message.chat_id,
                    text='Hi! Ich bin dein Wetterbot 😍 Was willst du wissen?  '
                         'Antworte /cancel um mich zu stoppen 😉\n\n')

    return REPLY

def reply(bot, update):
    extr_request = extractor.get_args(update.message.text)
    bot.sendMessage(update.message.chat_id,text="Ich schaue mal nach 😊")
    bot.sendMessage(update.message.chat_id,text=weather.deliver(*extr_request))
    return START


def next_question(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='Kann ich dir sonst noch helfen? 🙄')

    return REPLY


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s" % (user.first_name, 'user_photo.jpg'))
    bot.sendMessage(update.message.chat_id, text='Gorgeous! Now, send me your location please, '
                                                 'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo." % user.first_name)
    bot.sendMessage(update.message.chat_id, text='I bet you look great! Now, send me your '
                                                 'location please, or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f"
                % (user.first_name, user_location.latitude, user_location.longitude))
    bot.sendMessage(update.message.chat_id, text='Maybe I can visit you sometime! '
                                                 'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location." % user.first_name)
    bot.sendMessage(update.message.chat_id, text='You seem a bit paranoid! '
                                                 'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    bot.sendMessage(update.message.chat_id,
                    text='Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: [RegexHandler('^(Boy|Girl|Other)$', gender)],

            REPLY: [MessageHandler([Filters.text], reply)],

            NEXT_QUEST: [MessageHandler([Filters.text], reply)],

            LOC_UNKNOWN: [MessageHandler([Filters.photo], photo),
                    CommandHandler('skip', skip_photo)],

            TIME_UNKNOWN: [MessageHandler([Filters.location], location),
                       CommandHandler('skip', skip_location)],

            LOC_TIME_UNKNOWN: [MessageHandler([Filters.text], bio)]

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
