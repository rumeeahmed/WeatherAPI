from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app = Flask(__name__)


def get_weather(city: str) -> dict:
    api_key = os.environ.get('API_KEY')
    url = 'https://api.openweathermap.org/data/2.5/forecast?'
    response = requests.get(f'{url}q={city}&APPID={api_key}')


@app.route('/ping')
def ping():
    """
    Endpoint to check if the service is working.
    :return: JSON object containing details about the API.
    """
    ping_dict = {
        "name": "weatherservice",
        "status": "ok",
        "version": "1.0.0"
    }
    return jsonify(ping=ping_dict)


@app.route('/forecast/<city>')
def forecast(city: str):
    get_weather(city)

    # return jsonify(ping=ping_dict)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
