#! /usr/bin/env python

# Author: Phuc Tran Truong
# Date: 03.07.2016
# Wetter Bot
import weather
import extractor

print('Was möchtest du über das Wetter wissen?')
request = input('>>> ')
extr_request = extractor.get_args(request)
print(weather.deliver(*extr_request))
