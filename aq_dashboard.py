"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask 

app = Flask(__name__) 

@app.route('/')
def root():
    """Base view."""
    return 'TODO - part 2 and beyond!'