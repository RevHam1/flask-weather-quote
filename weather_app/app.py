# 1) Iimport the necessary Items for app
import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from waitress import serve

load_dotenv()

# 2) Initialize Flask app
app = Flask(__name__)

# 3) Initialize Routes & their logic


def get_random_quote():
    response = requests.get('https://api.quotable.io/random', verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return


@app.route('/')
@app.route('/index')
def index():
    quote = get_random_quote()
    return render_template('index.html', quote=quote)


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={
        city}&appid={os.getenv("API_KEY")}&units=imperial'
    response = requests.get(url)
    weather_data = response.json()

    response.json()

    if weather_data.get('cod') != 200:
        weather_info = {
            'error': 'City not found!'
        }
    else:
        weather_info = {
            'city': weather_data['name'],
            'temperature': f"{weather_data['main']['temp']: .1f}",
            'description': weather_data['weather'][0]['description'].capitalize(),
            'icon': weather_data['weather'][0]['icon'],
            'feels_like': f"{weather_data['main']['feels_like']: .1f}",
        }

    return render_template('weather.html', weather_info=weather_info)


# 4) Initialize Server
if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)
    # app.run(debug=True)
