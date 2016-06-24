#! /usr/bin/env python

# Autor: Phuc Tran Truong
# Datum: 14.06.2016
# Wetter Bot
import weather
import extractor

print('Was möchtest du zum Wetter wissen?')
request = input('time, place, type of query:  ')
print(weather.deliver())
