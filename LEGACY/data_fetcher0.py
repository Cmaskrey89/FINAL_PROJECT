import requests
from datetime import datetime, timezone, timedelta
import csv

# Base URLs
tide_base_url = "https://api.stormglass.io/v2/tide/sea-level/point"
weather_base_url = "https://api.stormglass.io/v2/weather/point"

# Your location parameters
latitude = -12.131991
longitude = -77.038901

# Current UTC time
current_day_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
current_day_end = current_day_start + timedelta(days=1)

# Function to compute average across sources
def compute_average(data_dict):
    values = list(data_dict.values())
    return sum(values) / len(values)

# Fetch tide data
response_tide = requests.get(
    tide_base_url,
    params={
        'lat': latitude,
        'lng': longitude,
        'start': current_day_start.isoformat(),
        'end': current_day_end.isoformat(),
    },
    headers={
        'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
    }
)
# Check if the tide API call was successful
if response_tide.status_code == 200:
    tide_data = response_tide.json()['data']
    tide_dict = {item['time']: item['sg'] for item in tide_data}
else:
    print(f"Tide API Error {response_tide.status_code}: {response_tide.text}")
    tide_dict = {}

# Fetch swell data
response_weather = requests.get(
    weather_base_url,
    params={
        'lat': latitude,
        'lng': longitude,
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
    headers={
        'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
    }
)

if response_weather.status_code == 200:
    weather_data = response_weather.json()
    hours = weather_data['hours']

    # Write data to CSV
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
            row['tideHeight'] = tide_dict.get(time, None)

            writer.writerow(row)

    print("Data saved to Hourly_Forecast.csv")

else:
    print(f"Error {response_weather.status_code}: {response_weather.text}")
