#!/usr/bin/python3
"""
View for city
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_of_state(state_id):
    """
    Retrieves cities of a state
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state_cities = state.cities
    cities_dicts = []
    for city in state_cities:
        cities_dicts.append(city.to_dict())
    return jsonify(cities_dicts)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieves a city object
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """
    Deletes a City object
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.json:
        return jsonify('Not a JSON'), 400
    if 'name' not in request.json:
        return jsonify('Missing name'), 400
    city = City(state_id=state_id, **request.get_json())
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_by_id(city_id):
    """
    Updates a City object
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key != 'id' and key != 'state_id' != 'created_at' and key != 'updated_at':
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
