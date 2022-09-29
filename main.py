import requests
import configparser


class NoSuchLocation(Exception):
    pass


user_input = input("Enter zip code: ")


def get_apikey():
    config = configparser.ConfigParser()
    config.read('app.config')
    apikey_from_file = config['secrets']['apikey']
    return apikey_from_file


# Gets users location based of zip entered
def get_location():
    location_url = 'https://dataservice.accuweather.com/locations/v1/' \
                   f'postalcodes/search?apikey={api_key}&q={user_input}'
    response = requests.get(location_url)

    try:
        key = response.json()[0].get('Key')
    except IndexError:
        raise NoSuchLocation()
    return key


# Gets the conditions of the zip entered
def get_conditions(key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/{}' \
                     f'?apikey={api_key}'.format(key)
    response = requests.get(conditions_url)
    json_version = response.json()

    print("Current Conditions:", json_version[0]['WeatherText'])


# Gets temperature of the zip entered
def get_temperature(key):
    temperature_url = 'https://dataservice.accuweather.com/currentconditions/v1/{}' \
                      f'?apikey={api_key}'.format(key)
    response = requests.get(temperature_url)
    json_version = response.json()
    print("Current Temperature:", json_version[0]['Temperature']['Imperial']['Value'], "F")


# Gets the forecast of the next 5 days
def get_fivedayforecast(key):
    fiveDayForecast_url = 'https://dataservice.accuweather.com/forecasts/v1/daily/5day/{}' \
                          f'?apikey={api_key}'.format(key)
    response = requests.get(fiveDayForecast_url)
    json_version = response.json()
    forecasts = json_version['DailyForecasts']
    for forecast in forecasts:
        print(forecast['Date'])
        print("Temperature:", forecast['Temperature']['Maximum']['Value'], 'F')
        print("Conditions:", forecast['Day']['IconPhrase'])


try:
    api_key = get_apikey()
    location_key = get_location()
    get_conditions(location_key)
    get_temperature(location_key)
    get_fivedayforecast(location_key)
except NoSuchLocation:
    print("Unable to get the location")
