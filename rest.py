import json
import math

import flask
from flask import Flask, request
import requests

app = Flask(__name__)

DB_API_SELECT_ALL_PLACES_URL = ''  # todo


@app.route('/')
def index():
    food = request.args.get('food')
    if food is None:
        return 'Required parameter not found: \'food\''
    location = request.args.get('location')
    if location is None:
        return 'Required parameter not found: \'location\''

    food = food.split(',')
    location = location.split(',')
    user_location_x, user_location_y = location[0], location[1]

    json_str = requests.get(DB_API_SELECT_ALL_PLACES_URL).content
    json_dict = json.loads(json_str)

    places = json_dict['places']

    for place in places[:]:
        tags = place.place_tags.split(',')
        matching_tags = [tag for tag in tags if tag in food]
        if len(food) != len(matching_tags):
            places.remove(place)

    places_by_distance = []
    for place in places:
        place_location_x, place_location_y = place['location']['x'], place['location']['y']
        distance = math.sqrt((place_location_x - user_location_x) ** 2 + (place_location_y - user_location_y) ** 2)
        places_by_distance.append((distance, place))

    places_by_distance.sort(key=lambda x: x[0], reverse=True)
    best_place = places_by_distance[0][1]

    # todo: consider score also

    return flask.jsonify(**best_place)


app.run()
