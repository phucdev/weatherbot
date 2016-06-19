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
- Wie kalt ist es in Moskau?
- Ist es sonnig?
- Brauche ich eine Jacke?

Das Projekt sollte kleine Tippfehler behandeln können und bei sonstigen Fehlern eine entsprechende Fehlermeldung schicken.
Einfache Negation in der Frage sollte beachtet werden und Aussagesätze zum Wetter statt Fragen sollten mit True/False beantwortet werden können bzw. “Das ist richtig.”, “Nein, das stimmt so nicht.”

## Python Module und APIs
##### NTLK
Im Kurs wurde viel mit dem Natural Language Toolkit (http://www.nltk.org/) gearbeitet. Deshalb wird es auch für dieses Projekt verwendet.
Das Python-Modul kann man ganz einfach mit diesem Befehl installieren:<br> 
`python3 -m pip install nltk`

##### OpenWeatherAPI, pyowm
Für das Projekt wird die OpenWeatherMAP API benutzt. Für einen API Key muss man sich dort registrieren. Es gibt einen kostenlosen Plan. 
Als Hilfsmittel wird das Python Modul “pyowm” verwendet.<br>
https://pyowm.readthedocs.io/en/latest/ <br>
Konkret interessant werden wohl diese Teile der Dokumentation sein: <br>
https://pyowm.readthedocs.io/en/latest/pyowm.webapi25.html#module-pyowm.webapi25.observation <br>
https://pyowm.readthedocs.io/en/latest/pyowm.utils.html <br>

Das Python-Modul kann man ganz einfach mit diesem Befehl installieren: 
`python3 -m pip install pyowm`

Ein Anfang wäre:
~~~~
import pyowm
# API Key
owm = pyowm.OWM('hier API einfügen')
observation = owm.weather_at_place("Berlin,de")
w = observation.get_weather()
# Temperatur
print(w.get_temperature('celsius')['temp'])
~~~~
Das Ding gibt die momentane Temperatur in Berlin aus. Das Skript owmtest.py ist noch ein wenig ausführlicher und zeigt weitere Funktionalitäten von pyowm.

##### Telegram Bot API
Idealerweise hätte das Projekt eine GUI mit Antworten, die mit graphischen Elemente (Symbole für Regen, Sonne usw.) geschmückt werden.
Eine andere Möglichkeit wäre, das Ganze in Form eines Bots auf Telegram oder auf Facebook Messenger zu implementieren.
Ich würde die Telegram API bevorzugen, da man sich auf Facebook Messenger als Facebook Developer registrieren muss.
Die Telegram Bot API: https://core.telegram.org/bots

Mockup als Telegram-Bot
![Wetterbot](/iOS Mockup.png?raw=true "Als Bot in Telegram")

## Struktur des Projekts und zentrale Probleme

### Struktur

##### wetterbot.py
Dieses Skript sollte die ganze Anbindung an die Telegram Bot API (Interaktion mit der API und dem User) bzw. die ganze Steuerung übernehmen.

##### extractor.py
Dieses Skript sollte den Input verarbeiten und an weather.py schicken. Bei Fragen, wo der Ort nicht spezifiziert wird, sollte nachgefragt werden oder wenn es geht, dann sollte der Ort automatisch durch Geo-Location bestimmt werden. Diesen soll der Bot bzw. das Programm sich für darauf folgende Fragen merken.

##### weather.py
Die Anbindung an die Wetter API ist nicht schwer, weil das Python Modul OWM die meiste Arbeit für uns erledigt. Also an die Wetterdaten ranzukommen ist relativ einfach.
Das Python Skript weather.py übernimmt da die ganze Arbeit. Alle weiteren Wetter-Funktionen sollten dort reingeschrieben werden.

Im Wesentlichen gibt es drei Variablen:
- place → Ort
- time → Zeit 
- query → Typ von Abfrage (Wetter, Temperatur, sunny?, rainy?, random)  

### Probleme
Das Schwierigste ist tatsächlich die Verarbeitung des Inputs (extractor.py).
- Ort erkennen
- Zeit erkennen
- Art der Wetterabfrage erkennen
- Rechtschreibfehler erkennen, behandeln (ideal: “Meintest du vielleicht?”)
- ungültigen Input behandeln

Ein weiteres Problem ist die Anbindung an die Telegram Bot API, weil ich noch keine Erfahrung damit habe.
- Output im Bot (wetterbot.py)
