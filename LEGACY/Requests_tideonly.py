import arrow
import requests

# Your location parameters
latitude = -12.131991
longitude = -77.038901

# Current UTC time
current_day_start = arrow.now().floor('day')
current_day_end = arrow.now().shift(days=1).floor('day')

response = requests.get(
    'https://api.stormglass.io/v2/tide/sea-level/point',
    params={
        'lat': latitude,
        'lng': longitude,
        'start': current_day_start.to('UTC').timestamp(),  # Convert to UTC timestamp
        'end': current_day_end.to('UTC').timestamp(),  # Convert to UTC timestamp
    },
    headers={
        'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'    }
)

# Check if the request was successful
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print(f"Error {response.status_code}: {response.text}")
