#!bin/python

import flask
import os

from services import Services

app = flask.Flask(__name__, static_folder='public')

@app.route('/')
def index():
    s = Services('http://www.ipma.pt')
    placeRef = flask.request.args.get('placeRef')
    if placeRef:
        w = s.get_place_weather(1)
        if w is None:
            flask.abort(404) # not found
        else:
            selectedPlace = PlaceWeather("some-description", w)
    else:
        selectedPlace = None


    places = Services.placeMap.values()
    rvalue = flask.render_template('index.jinja', places=places, selectedPlace=selectedPlace)
    return rvalue



class PlaceWeather(object):
    def __init__(self, description, weather):
        self.description = description
        self.weather = weather
        return

if __name__ == '__main__':
    app.run(debug=True,port=8080)
