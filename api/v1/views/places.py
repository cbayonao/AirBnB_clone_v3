#!/usr/bin/python3
"""
View for state
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_for_city(city_id):
    """
    retrieve an object into a valid JSON
    """
    my_list = []
    all_cities = storage.all(City)
    for city in all_cities:
        if all_cities[city].id == city_id:
            for obj in all_cities:
                my_list.append(all_places[obj].to_dict())
            return jsonify(my_list)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieves a Place object: GET /api/v1/places/<place_id>
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place accord the city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        return jsonify('Missing user_id'), 400
    user = storage.get("User", request.get_json()["user_id"])
    if not user:
        abort(404)
    if "name" not in request.get_json():
        return jsonify("Missing name"), 400
    place = Place(**request.get_json())
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """
    Updates a Place object
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_at',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
