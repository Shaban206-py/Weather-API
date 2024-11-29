from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

# Create your views here.
def home(request):
    # Set default city to 'Islamabad' if not provided
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Islamabad'

    # Weather API URL
    urls = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=418c92de47270c6b7fa25a4e551b5554'
    PARAMS = {'units': 'metric'}

    # Google Custom Search API parameters
    API_KEY = 'AIzaSyCsg6At9vkg9AkE_iPAsn7FKRY89ULIAJ4'
    SEARCH_ENGINE_ID = 'c70eb0f5dc02e4efa'
    query = city + " 1920x1080"  # Image search query with resolution
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        # Request to the Google Custom Search API
        data = requests.get(city_url).json()

        # Check if 'items' exists in the response
        search_items = data.get("items", [])
        if search_items:
            # Get the image URL from the search items (use 'link' instead of 'Link')
            image_url = search_items[0]['link']
        else:
            # If no items found, set a default image URL (fallback)
            image_url = "https://example.com/default_image.jpg"

    except KeyError as e:
        # Handle the case when the 'items' or 'link' key is not found
        image_url = "https://example.com/default_image.jpg"
        messages.error(request, f"Error retrieving image: {str(e)}")

    try:
        # Request to the OpenWeatherMap API for weather data
        data = requests.get(urls, params=PARAMS).json()

        # Extract relevant weather data from the API response
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        # Render the template with weather data and image URL
        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        # If there's an error with weather data (e.g., invalid city), display a fallback
        exception_occurred = True
        messages.error(request, 'You might have entered the wrong city.')
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'Islamabad',
            'exception_occurred': exception_occurred,
            'image_url': image_url  # Default or fallback image URL
        })
