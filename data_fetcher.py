import requests
from datetime import datetime, timezone, timedelta
import csv

############ DEFINITIONS ############

# API URLs for both the TIDE data and WEATHER data
TIDE_BASE_URL = "https://api.stormglass.io/v2/tide/sea-level/point"
WEATHER_BASE_URL = "https://api.stormglass.io/v2/weather/point"

# Reventazon de Makaha precise location based on google maps.
LATITUDE = -12.131991
LONGITUDE = -77.038901

# Free AUTH for Stormglass API
AUTH_HEADER = {
    'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
}

# Stormglass data is in UTC, so need to define the PET timezone as UTC-5
pet_timezone = timezone(timedelta(hours=-5))

# Use datetime and timedelta functions from datetime library to calculate current day's start and end in PET (shouldve probably used arrow...)
# Initially I decided to get data from the future but ultimately I decided to get the data from TODAY only. It's gonna be a forecast for those looking to surf TODAY! 
CURRENT_DAY_START_PET = datetime.now(pet_timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
CURRENT_DAY_END_PET = CURRENT_DAY_START_PET + timedelta(days=1) - timedelta(seconds=1)  # Adjusted to 23:59:59

############ DEFINITION OF TIDE FETCHING FUNCTION ############

#Main Function

def fetch_tide_data():
    response_tide = requests.get(
        TIDE_BASE_URL,
        params={
            'lat': LATITUDE,
            'lng': LONGITUDE,
            'start': CURRENT_DAY_START_PET.isoformat(),
            'end': CURRENT_DAY_END_PET.isoformat(),
            'datum': 'MLLW'
        },
        headers=AUTH_HEADER
    )

# If succesful fetch, we save into tide_data

    if response_tide.status_code == 200:
        tide_data = response_tide.json()['data']
        print("Tide Data:", tide_data)  # Printing for debugging !
        return {item['time']: item['sg'] for item in tide_data}
    else:
        print(f"Tide API Error whoops! {response_tide.status_code}: {response_tide.text}")
        return {}
    
############ DEFINITION OF WEATHER FETCHING FUNCTION ############

#Main Function

def fetch_weather_data():
    response_weather = requests.get(
        WEATHER_BASE_URL,
        params={
            'lat': LATITUDE,
            'lng': LONGITUDE,
            'params': ','.join([
                'swellDirection', 
                'swellHeight', 
                'swellPeriod', 
                'secondarySwellPeriod', 
                'secondarySwellDirection', 
                'secondarySwellHeight',
                'windWaveHeight',
                'windWavePeriod',
                'windDirection',
                'windSpeed'
            ]),
            'start': CURRENT_DAY_START_PET.isoformat(),
            'end': CURRENT_DAY_END_PET.isoformat()
        },
        headers=AUTH_HEADER
    )

# If succesful fetch, we save into weather_data 
    
    if response_weather.status_code == 200:
        weather_data = response_weather.json()
        print("Weather Data:", weather_data) # Print for debugging
        return weather_data
    else:
        print(f"Weather API Error whoops! {response_weather.status_code}: {response_weather.text}")
        return None

############ DEFINITION OF SUPPORT FUNCTIONS ############

#Get data from sg (stormglass) source, which chooses the most accurate data source for any location.

def get_sg_data(param_dict):
    return param_dict['sg'] if 'sg' in param_dict else None

############ FUNCTION TO SAVE FETCHED DATA INTO CSV FILE ############

def save_data_to_csv(weather_data, tide_data):
    hours = weather_data['hours'] #we get the time data from weather_data but it could be either way!

# These are the fieldnames we will need, basically tide + weather data and in this order.
    with open('Hourly_Forecast.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'time', 
            'swellHeight', 
            'swellPeriod',
            'swellDirection',
            'secondarySwellPeriod', 
            'secondarySwellDirection', 
            'windWaveHeight',
            'windWavePeriod',
            'windDirection',
            'windSpeed',
            'tideHeight'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

#probably not the clearest code but it does the job, at the end I found I could filter the sg data directly from the API call but its done now!
        for hour in hours:
            row = {'time': hour['time']}
            for param in fieldnames[1:-1]: # 1 to -1 to include all elements in fieldnames except the first and the last
                if param in hour:
                    row[param] = get_sg_data(hour[param]) * 3.6 if param == 'windSpeed' else get_sg_data(hour[param]) #transform windspeed from knots to km/h
            row['tideHeight'] = tide_data.get(hour['time'], None)

            print("Row Data:", row)  # Debugging line to print each row's data
            writer.writerow(row)

    print("You data has been saves to Hourly_Forecast.csv :) kind ser/madame")

############ MAIN FUNCTION ############

def main():
    tide_data = fetch_tide_data()
    weather_data = fetch_weather_data()

    if weather_data: #We assume that if one is working the other is too.
        save_data_to_csv(weather_data, tide_data)

# Enable the script ro run as stand-alone or as be called by another script (app.py)
if __name__ == "__main__":
    main()
