import pyowm

owm = pyowm.OWM('0ce70d38fc4aaade9c6f004e226e8a61')  # You MUST provide a valid API key


# Will it be sunny tomorrow at this time in Berlin (Germany) ?
# returns forecaster
forecast = owm.daily_forecast("Berlin,de")
# alternatively: owm.three_hours_forecast("Berlin, de")
# timeutils, returns date.datetime object
now = pyowm.timeutils.now()
tomorrow = pyowm.timeutils.tomorrow()
yesterday = pyowm.timeutils.yesterday()
print(forecast)
print("Sunny: ", forecast.will_be_sunny_at(now))

# Search for current weather in Berlin (de)
observation = owm.weather_at_place('Berlin,de')
w = observation.get_weather()
#w = forecast.get_weather_at(now)
print(w)

# Weather details
# int: GMT UNIX time of weather measurement
print("Reference Time: ", pyowm.utils.timeformatutils.to_ISO8601(w.get_reference_time()))
# int: GMT UNIX time of sunrise
print("Sunrise: ", pyowm.utils.timeformatutils.to_ISO8601(w.get_sunrise_time()))
# int: GMT UNIX time of sunset
print("Sunset: ", pyowm.utils.timeformatutils.to_ISO8601(w.get_sunset_time()))
# int: cloud coverage percentage
print("Clouds: ", w.get_clouds())
# dict: precipitation info
print("Rain: ", w.get_rain())
# dict: snow info
print("Snow: ", w.get_snow())
# dict: wind info
print("Wind: ", w.get_wind())
# int: atmospheric humidity percentage
print("Humidity: ", w.get_humidity())
# int: atmospheric pressure info
print("Pressure: ", w.get_pressure())
# dict: temperature info
print("Temperature: ", w.get_temperature('celsius'))
# Unicode: short weather status
print("Status: ", w.get_status())
# Unicode: detailed weather status
print("Detailed Status: ", w.get_detailed_status())
# int: OWM weather condiction code
print("Weather Code: ", w.get_weather_code())
# Unicode: weather-related icon name
print("Weather Icon Name: ", w.get_weather_icon_name())
# float: visibility distance
print("Visibility Distance: ", w.get_visibility_distance())
# float: dewpoint
print("Dewpoint: ", w.get_dewpoint())
# float: Canadian humidex
print("Humidex: ", w.get_humidex())
# float: heat index
print("Heat Index: ", w.get_heat_index())

# Search current weather observations in the surroundings of
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
# observation_list = owm.weather_around_coords(-22.57, -43.12)
# print(observation_list)
