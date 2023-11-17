import requests
from datetime import datetime, timezone

# Endpoint and parameters
base_url = "https://api.stormglass.io/v2/weather/point"
latitude = -12.131991  # Lima
longitude = -77.038901  # Lima

# Current UTC time rounded to the closest hour
current_hour = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

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
    'start': current_hour.isoformat(),
    'end': current_hour.isoformat()
}

# Headers with your API key
headers = {
    'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'
}

response = requests.get(base_url, params=params, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
