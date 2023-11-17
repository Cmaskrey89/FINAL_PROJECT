import requests
from datetime import datetime, timezone
import csv

base_url = "https://api.stormglass.io/v2/weather/point"

# Your location parameters
latitude = -12.131991
longitude = -77.038901

# Current UTC time
current_day_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
current_day_end = current_day_start.replace(hour=23, minute=59, second=59)

params = {
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
}

headers = {
    'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'  # Make sure to use your correct API key
}

response = requests.get(base_url, params=params, headers=headers)

# Function to compute average across sources
def compute_average(data_dict):
    values = list(data_dict.values())
    return sum(values) / len(values)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extracting hours data
    hours = data['hours']

    # Writing to a CSV file
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
            'windSpeed'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for hour in hours:
            row = {'time': hour['time']}
            for param in fieldnames[1:]:
                if param == 'windSpeed' and param in hour:
                    row[param] = compute_average(hour[param]) * 3.6  # Convert wind speed from m/s to km/h
                else:
                    row[param] = compute_average(hour[param]) if param in hour else None
            writer.writerow(row)

    print("Data saved to Hourly_Forecast.csv")

else:
    print(f"Error {response.status_code}: {response.text}")
