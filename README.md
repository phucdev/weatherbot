# Wetterbot
Interprets questions about the weather in natural language and (hopefully) delivers adequate information about the weather. 
This is a group project that I'll be doing for the course "Einführung in die maschinelle Sprachverarbeitung mit Python". 
In the initial phase it will only work with German input. 
The rest of the readme.md will be in German.

## Einführung
Das Projekt soll Wetterabfragen in natürlicher Sprache bearbeiten und adäquate Antworten liefern.<br>
Beispiele für Fragen sind: 
- Regnet es?
- Wie warm ist es in Berlin?
- Wie ist das Wetter am Dienstag?
- Ist es morgen sonnig?

User-Abfragen, die nichts mit dem Wetter zu tun haben, sollten auch behandelt werden können.

## Python Module, APIs und andere Hilfsmittel
Für das Projekt wurden folgende APIs und Module benutzt:
- OpenWeatherAPI (http://openweathermap.org/api), pyowm (https://github.com/csparpa/pyowm) für die Wetterdaten
- ipinfo (http://ipinfo.io), requests (http://docs.python-requests.org/en/master/) für die Bestimmung des Ortes via IP-Adresse
- NLTK (http://www.nltk.org), StanfordNERTagger (http://nlp.stanford.edu/software/CRF-NER.shtml) für die Verarbeitung des User-Inputs
- Telegram Bot API (https://core.telegram.org/bots/api), python-telegram-bot (https://github.com/python-telegram-bot/python-telegram-bot) für die Realisierung als Telegram Bot

### Telegram Bot
Den Wetterbot findet ihr unter http://telegram.me/phucbot.

Mockup als Telegram-Bot
![Wetterbot](https://raw.githubusercontent.com/phucdev/weatherbot/master/Telegram-Mockup.jpg)

## Struktur des Projekts und zentrale Probleme

### Struktur

##### main.py
Dieses Skript sollte die ganze Anbindung an die Telegram Bot API (Interaktion mit der API und dem User) bzw. die ganze Steuerung übernehmen. Das Skript muss laufen, damit der Wetterbot funktioniert. Hier haben wir uns vom Conversationbot-Beispiel (https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py) inspirieren lassen.

##### extractor.py
Dieses Skript sollte den Input verarbeiten und an weather.py schicken. Bei Fragen, wo der Ort nicht spezifiziert wird, sollte nachgefragt werden oder wenn es geht, dann sollte der Ort automatisch durch Geo-Location bestimmt werden.

##### weather.py
Die Anbindung an die Wetter API ist nicht schwer, weil das Python Modul OWM die meiste Arbeit für uns erledigt. Also an die Wetterdaten ranzukommen ist relativ einfach.
Das Python Skript weather.py übernimmt da die ganze Arbeit. Alle weiteren Wetter-Funktionen sollten dort reingeschrieben werden.

Im Wesentlichen gibt es drei Variablen:
- place → Ort durch StanfordNERTagger
- time → Zeit durch Keyword-Erkennung
- query → Typ von Abfrage (Wetter, Temperatur, sunny?, rainy?, random)  durch Keyword-Erkennung 

### Probleme
Das Schwierigste ist tatsächlich die Verarbeitung des Inputs (extractor.py). Momentan gibt es noch folgende Probleme:
- ungültige Orte erkennen (bsp.: "in Entenhausen")
- komplexe Zeit erkennen (Uhrzeiten wie "17:30 Uhr" oder "3 Uhr nachmittags")
- ungültigen Input, Mehrfachangaben behandeln
