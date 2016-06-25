#! /usr/bin/env python

# Autor: Phuc Tran Truong
# Datum: 25.06.2016
# Wetter Bot
import weather
import extractor

# Starre Reihenfolge, nur drei Argumente
print('Aktuell/Morgen Ort Wetter/Temperatur')
request = input('>>> ')
extr_request = extractor.get_args(request)
try:
    print(weather.deliver(*extr_request))
except TypeError:
    print(weather.deliver(extr_request[0],extr_request[1],extr_request[2]))
