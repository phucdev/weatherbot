#! /usr/bin/env python

# Autor: Phuc Tran Truong
# Datum: 14.06.2016
# Wetter Bot
import weather
place = input('Stadt?   ')
time = input('Aktuell/Morgen?   ')
query = input('Wetter/Temperatur?   ')
print(weather.deliver(place, time, query))
