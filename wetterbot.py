#! /usr/bin/env python

"""
Author: Phuc Tran Truong
Date: 14.07.2016

What it is supposed to do:
1. handle the Telegram Bot API: talk to the user
2. send input to extractor, retrieve info from weather

Wetter Bot
HTTP request: https://api.telegram.org/bot<token>/METHOD_NAME
xample: https://api.telegram.org/bot264478430:AAGUEm4KRnsMb3vTGZYSDzGhoLfe6WDX2BQ/getMe
"""
import weather
import extractor

# keywords to end the session
quit_exp = ['stop','ende', 'end', 'das wars']

# extract arguments from the input, retrieve weather data
def do_magic(request):
    extr_request = extractor.get_args(request)
    return weather.deliver(*extr_request)

# ask user
request = ''
while True:
    print('Was möchtest du über das Wetter wissen?')
    request = input('>>> ')
    # check for quit expressions
    if request in quit_exp:
        break
    print(do_magic(request))
print('Ok. Bye.')
