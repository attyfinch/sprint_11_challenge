"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from openaq import OpenAQ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


def get_results():
    '''
    Performs API GET request and pulls for results for pm25
    '''
    api = OpenAQ()
    status, body = api.measurements(parameter='pm25')
    results = body['results']
    utc_and_values = []

    for result in results:
        utc_and_values.append((result['date']['utc'], result['value']))

    return utc_and_values


class Record(DB.Model):
    '''Builds db schema'''
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String, nullable=False)
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'Id: {self.id}, Time: {self.datetime}, Value: {self.value}'


@app.route('/')
def root():
    """Base view.
    Return and display values >= 18
    """
    potentially_risky = Record.query.filter(Record.value >= 18).all()

    return f"{potentially_risky}"


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()

    values = get_results()

    for value in values:
        db_record = Record(datetime=value[0], value=value[1])
        DB.session.add(db_record)

    DB.session.commit()

    return str(values)
