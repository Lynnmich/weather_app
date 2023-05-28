
from flask import Flask, render_template, request
import requests
from datetime import datetime
from pytz import timezone

app = Flask(__name__)
api_key = "0bb67b102ce04e85aad53138232805"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
        response = requests.get(url)
        data = response.json()

        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        city_name = data['location']['name']
        current_day = datetime.now().strftime("%A")

        current_time = datetime.now().strftime("%H:%M:%S")
        time_zone = timezone('America/New_York')
        current_time_zone = datetime.now(time_zone).strftime("%H:%M:%S")

        return render_template('weather.html', city=city_name, temperature=temperature, description=description, current_time=current_time, current_time_zone=current_time_zone, current_day=current_day)

    # Handle GET request for displaying the form
    return render_template('index.html')

@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)