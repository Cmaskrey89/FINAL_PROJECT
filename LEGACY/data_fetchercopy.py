import requests
from datetime import datetime, timezone, timedelta
import csv
import arrow

# Base URLs
TIDE_BASE_URL = "https://api.stormglass.io/v2/tide/sea-level/point"
WEATHER_BASE_URL = "https://api.stormglass.io/v2/weather/point"

# Your location parameters
LATITUDE = -12.131991
LONGITUDE = -77.038901

AUTH_HEADER = {
    'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
}

start_pet = arrow.now('America/Lima').floor('day')  # Assuming PET is Lima time
end_pet = arrow.now('America/Lima').ceil('day')

start_utc = start_pet.to('UTC')
end_utc = end_pet.to('UTC')

def fetch_tide_data():
    response_tide = requests.get(
        TIDE_BASE_URL,
        params={
            'lat': LATITUDE,
            'lng': LONGITUDE,
            'start': start_utc.timestamp(),
            'end': end_utc.timestamp(),
            'datum': 'MLLW',
            'source': 'sg'
        },
        headers=AUTH_HEADER
    )
    if response_tide.status_code == 200:
        tide_data = response_tide.json()['data']
        print("Tide Data:", tide_data)  # Debugging line
        return {item['time']: item['sg'] for item in tide_data}
    else:
        print(f"Tide API Error {response_tide.status_code}: {response_tide.text}")
        return {}

def fetch_weather_data():
    response_weather = requests.get(
        WEATHER_BASE_URL,
        params={
            'lat': LATITUDE,
            'lng': LONGITUDE,
            'source': 'sg',
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
            'start': start_utc.timestamp(),
            'end': end_utc.timestamp(),
        },
        headers=AUTH_HEADER
    )
    if response_weather.status_code == 200:
        weather_data = response_weather.json()
        print("Weather Data:", weather_data)  # Debugging line
        return weather_data
    else:
        print(f"Weather API Error {response_weather.status_code}: {response_weather.text}")
        return None

def save_data_to_csv(weather_data, tide_data):
    hours = weather_data['hours']

    with open('Hourly_Forecast.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'time', 
            'swellHeight', 
            'swellPeriod',
            'swellDirection',
            'secondarySwellHeight',
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

        for hour in hours:
            row = {'time': hour['time']}
            for param in fieldnames[1:-1]:
                if param in hour:
                    row[param] = float(hour[param])* 3.6 if param == 'windSpeed' else float(hour[param])
            row['tideHeight'] = tide_data.get(hour['time'], None)

            print("Row Data:", row)  # Debugging line to print each row's data
            writer.writerow(row)

    print("Data saved to Hourly_Forecast.csv")

def main():
    tide_data = fetch_tide_data()
    weather_data = fetch_weather_data()

    if weather_data:
        save_data_to_csv(weather_data, tide_data)

if __name__ == "__main__":
    main()
