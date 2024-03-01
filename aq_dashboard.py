"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from openaq import OpenAQ   

app = Flask(__name__)


def get_results():
    api = OpenAQ()
    status, body = api.measurements(parameter='pm25')
    results = body['results']
    utc_and_values = []

    for result in results:
        utc_and_values.append((result['date']['utc'], result['value']))

    return utc_and_values

@app.route('/')
def root():
    """Base view."""

    return get_results()
