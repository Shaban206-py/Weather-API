# Weather App with Google Custom Search

This is a Django-based web application that provides weather information for a given city. It uses the OpenWeatherMap API to fetch weather data and Google Custom Search API to fetch a relevant image for the city. The app also provides fallback mechanisms for invalid city input and missing images.

## Features

- **Weather Information**: Displays the weather description, temperature, and an icon based on the city entered by the user.
- **City Image**: Fetches a high-resolution city image using Google Custom Search API.
- **Error Handling**: Handles errors related to city input (wrong city name) and image fetching with fallback options.
- **Spelling Correction**: Uses fuzzy matching to suggest the closest matching city if a small typo is made when entering the city name.

## Requirements

To run this project, you need:

- Python 3.x
- Django
- `requests` (for making API calls)
- `fuzzywuzzy` (for fuzzy matching city names)

### Install Dependencies

Install the necessary Python packages using pip:

```bash
pip install django requests fuzzywuzzy python-Levenshtein
Setup Instructions
Step 1: Clone the Repository
Clone the repository to your local machine:

bash
Copy code
git clone <repository_url>
cd <repository_directory>
Step 2: Set up Django Project
Make sure you have Django installed. If not, you can install it using pip:

bash
Copy code
pip install django
Run the following command to create a Django project:

bash
Copy code
django-admin startproject weatherproject
cd weatherproject
Then create an app inside the project:

bash
Copy code
python manage.py startapp weatherapp
Step 3: Update views.py File
Replace the content of your weatherapp/views.py file with the code below.

python
Copy code
from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
from fuzzywuzzy import process

# List of cities or use OpenWeatherMap's city list
city_list = ['Islamabad', 'Karachi', 'Lahore', 'New York', 'London', 'Paris', 'Tokyo', 'Sydney']

# Function to get the closest matching city
def get_closest_city(user_input, city_list):
    closest_match = process.extractOne(user_input, city_list)
    return closest_match[0]  # closest match city name

def home(request):
    # Set default city to 'Islamabad' if not provided
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Islamabad'

    # Check for spelling errors and find the closest matching city
    city = get_closest_city(city, city_list)

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
Step 4: Configure URLs
In the weatherapp/urls.py, make sure to map the home view to a URL:

python
Copy code
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
Then, in weatherproject/urls.py, include the weatherapp URLs:

python
Copy code
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weatherapp.urls')),
]
Step 5: Create Template
Create a template index.html in the weatherapp/templates/weatherapp/ directory to display the weather information and city image.

html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
</head>
<body>
    <h1>Weather for {{ city }}</h1>

    {% if exception_occurred %}
        <p>Error: {{ messages }}</p>
    {% else %}
        <p>Description: {{ description }}</p>
        <p>Temperature: {{ temp }}°C</p>
        <p>Day: {{ day }}</p>
        <img src="http://openweathermap.org/img/wn/{{ icon }}@2x.png" alt="{{ description }}">
        <img src="{{ image_url }}" alt="City Image" width="600">
    {% endif %}

    <form method="POST">
        {% csrf_token %}
        <label for="city">Enter City:</label>
        <input type="text" id="city" name="city" value="{{ city }}">
        <button type="submit">Get Weather</button>
    </form>
</body>
</html>
Step 6: Run the Development Server
Once everything is set up, run the Django development server:

bash
Copy code
python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/ to see the weather information for the specified city. You can also input a different city to see its weather and associated image.

Conclusion
This project allows users to check the weather of any city, providing a city image as well. It uses the OpenWeatherMap API for weather data and Google Custom Search for fetching images. The app also uses fuzzy matching to help handle slight typos in city names.
