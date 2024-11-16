import requests
from django.shortcuts import render

# Tomorrow.io API and Mapbox settings
TOMORROW_API_KEY = 'jr3CHKMMv2W8HZpbNerjQrl99WTp2QPM'
MAPBOX_TOKEN = 'pk.eyJ1IjoiaWJyYWhpbTU0NiIsImEiOiJjbTNqZGVzd2gwMnE3MmxyYjUzaWJ2anBzIn0.cGcOASzzXagrHTgTeqXWFw'

def home(request):
    weather_data = {}
    if request.method == 'POST':
        location = request.POST.get('location')
        if location:
            # Get coordinates from Mapbox Geocoding API
            mapbox_url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json'
            mapbox_params = {'access_token': MAPBOX_TOKEN, 'limit': 1}
            mapbox_response = requests.get(mapbox_url, params=mapbox_params)
            mapbox_data = mapbox_response.json()
            
            if mapbox_data['features']:
                coordinates = mapbox_data['features'][0]['geometry']['coordinates']
                place_name = mapbox_data['features'][0]['place_name']
                
                # Fetch weather data from Tomorrow.io
                tomorrow_url = f'https://api.tomorrow.io/v4/weather/realtime'
                tomorrow_params = {
                    'location': f'{coordinates[1]},{coordinates[0]}',
                    'apikey': TOMORROW_API_KEY,
                    'fields': 'temperature,temperatureApparent,precipitationIntensity,humidity,windSpeed,windDirection'
                }
                tomorrow_response = requests.get(tomorrow_url, params=tomorrow_params)
                weather = tomorrow_response.json()
                
                if 'data' in weather:
                    data = weather['data']['values']
                    weather_data = {
                        'place_name': place_name,
                        'temperature': data['temperature'],
                        'temperature_apparent': data['temperatureApparent'],
                        'precipitation': data.get('precipitationIntensity', 'N/A'),
                        'humidity': data['humidity'],
                        'wind_speed': data['windSpeed'],
                        'wind_direction': data['windDirection'],
                        'coordinates': coordinates,
                    }
                else:
                    weather_data['error'] = "Unable to fetch weather data."
            else:
                weather_data['error'] = "Invalid location entered."
        else:
            weather_data['error'] = "Please enter a location."
    
    return render(request, 'weather/home.html', {'weather_data': weather_data, 'mapbox_token': MAPBOX_TOKEN})
