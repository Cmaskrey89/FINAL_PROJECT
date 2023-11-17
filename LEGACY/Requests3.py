import requests
from datetime import datetime, timezone
import csv
import arrow

# Fetching tide data
def get_tide_data():
    tide_url = 'https://api.stormglass.io/v2/tide/sea-level/point'
    start = arrow.utcnow().floor('day')
    end = start.shift(days=1).floor('day')
    
    response = requests.get(
        tide_url,
        params={
            'lat': latitude,
            'lng': longitude,
            'start': start.timestamp(),
            'end': end.timestamp() - 1,
        },
        headers={
        'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
        }
    )
    
    if response.status_code == 200:
        return {point['time']: point['sg'] for point in response.json()['data']}
    else:
        print(f"Error fetching tide data: {response.status_code}: {response.text}")
        return {}

# Base URL and parameters for swell data
base_url = "https://api.stormglass.io/v2/weather/point"
latitude = -12.131991
longitude = -77.038901
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
    'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
}

response = requests.get(base_url, params=params, headers=headers)
tide_data = get_tide_data()

def compute_average(data_dict):
    values = list(data_dict.values())
    return sum(values) / len(values)

if response.status_code == 200:
    data = response.json()
    hours = data['hours']

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
            'tide'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for hour in hours:
            row = {'time': hour['time']}
            for param in fieldnames[1:-1]:  # Excluding tide for now
                if param == 'windSpeed' and param in hour:
                    row[param] = compute_average(hour[param]) * 3.6
                else:
                    row[param] = compute_average(hour[param]) if param in hour else None
            row['tide'] = tide_data.get(hour['time'], None)  # Fetching tide data
            writer.writerow(row)

    print("Data saved to Hourly_Forecast.csv")

else:
    print(f"Error {response.status_code}: {response.text}")
