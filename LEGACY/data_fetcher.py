import requests
from datetime import datetime, timezone, timedelta
import csv

# Base URLs
TIDE_BASE_URL = "https://api.stormglass.io/v2/tide/sea-level/point"
WEATHER_BASE_URL = "https://api.stormglass.io/v2/weather/point"

# Your location parameters
LATITUDE = -12.131991
LONGITUDE = -77.038901

AUTH_HEADER = {
    'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
}


# Function to compute average across sources
def compute_average(data_dict):
    values = list(data_dict.values())
    return sum(values) / len(values)


def fetch_tide_data():
    current_day_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    current_day_end = current_day_start + timedelta(days=1)

    response_tide = requests.get(
        TIDE_BASE_URL,
        params={
            'lat': LATITUDE,
            'lng': LONGITUDE,
            'start': current_day_start.isoformat(),
            'end': current_day_end.isoformat(),
        },
        headers=AUTH_HEADER
    )
    if response_tide.status_code == 200:
        tide_data = response_tide.json()['data']
        return {item['time']: item['sg'] for item in tide_data}
    else:
        print(f"Tide API Error {response_tide.status_code}: {response_tide.text}")
        return {}


def fetch_weather_data():
    current_day_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    current_day_end = current_day_start + timedelta(days=1)

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
            'start': current_day_start.isoformat(),
            'end': current_day_end.isoformat()
        },
        headers=AUTH_HEADER
    )
    if response_weather.status_code == 200:
        return response_weather.json()
    else:
        print(f"Error {response_weather.status_code}: {response_weather.text}")
        return None


def save_data_to_csv(weather_data, tide_data):
    hours = weather_data['hours']

    with open('Hourly_Forecast.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'time',
            'swellDirection', 
            'swellHeight', 
            'swellPeriod', 
            'secondarySwellPeriod', 
            'secondarySwellDirection', 
            'secondarySwellHeight',
            'windWaveHeight',
            'windWavePeriod',
            'windDirection',
            'windSpeed',
            'tideHeight'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for hour in hours:
            time = hour['time']
            row = {'time': time}

            for param in fieldnames[1:-1]:
                if param == 'windSpeed' and param in hour:
                    row[param] = compute_average(hour[param]) * 3.6  # Convert from m/s to km/h
                else:
                    row[param] = compute_average(hour[param]) if param in hour else None

            # Add tide data
            row['tideHeight'] = tide_data.get(time, None)

            writer.writerow(row)

    print("Data saved to Hourly_Forecast.csv")


def main():
    tide_data = fetch_tide_data()
    weather_data = fetch_weather_data()

    if weather_data:
        save_data_to_csv(weather_data, tide_data)


if __name__ == "__main__":
    main()
