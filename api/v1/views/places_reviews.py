#!/usr/bin/python3
"""
View for state
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_for_place(place_id):
    """
    retrieve an object into a valid JSON
    """
    my_list = []
    plac = storage.all(Place)
    for p in plac:
        if plac[p].id == place_id:
            var = plac[p].reviews
            for i in var:
                my_list.append(i.to_dict())
            return (jsonify(my_list))
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_id(review_id):
    """
    Retrieves a Place object: GET /api/v1/places/<place_id>
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review accord the place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        return jsonify('Missing user_id'), 400
    user = storage.get("User", request.get_json()["user_id"])
    if not user:
        abort(404)
    if "text" not in request.get_json():
        return jsonify("Missing text"), 400
    review = Review(**request.get_json())
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
