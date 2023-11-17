import requests
import arrow

# Your location parameters
latitude = -12.131991
longitude = -77.038901

# Current day's start and end times in UTC
start = arrow.utcnow().floor('day')
end = start.shift(days=1).floor('day')

response = requests.get(
    'https://api.stormglass.io/v2/tide/sea-level/point',
    params={
        'lat': latitude,
        'lng': longitude,
        'start': start.timestamp(),
        'end': end.timestamp() - 1,  # Subtract a second to get 23:59:59
    },
    headers={
        'Authorization': '32077ffa-6b91-11ee-92e6-0242ac130002-3207805e-6b91-11ee-92e6-0242ac130002'    }
    
)

# Check the status and print the data
if response.status_code == 200:
    json_data = response.json()
    for data_point in json_data['data']:
        print(data_point)
else:
    print(f"Error {response.status_code}: {response.text}")
