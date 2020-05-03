#!/usr/bin/python3
"""
View for user
"""
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """
    Retrieves all users
    """
    all_users = storage.all(User)
    my_list = []
    for obj in all_users:
        my_list.append(all_users[obj].to_dict())
    return jsonify(my_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieves a User object: GET /api/v1/users/<user_id>
    """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Deletes a User object
    """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Creates a User: POST /api/v1/users
    """
    if not request.json:
        return jsonify('Not a JSON'), 400
    if 'email' not in request.json:
        return jsonify('Missing email'), 400
    if 'password' not in request.json:
        return jsonify('Missing password'), 400
    user = User(**request.get_json())
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id):
    """
    Updates a User object
    """
    user = storage.get("User", user_id)
    print(user)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if (key != 'id' and
                key != 'email' and
                key != 'created_at' and
                key != 'updated_at'):
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
#    return make_response(jsonify(user.to_dict()), 200)
