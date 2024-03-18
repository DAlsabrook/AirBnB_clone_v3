#!/usr/bin/python3
"""
Module to handle the review class routes
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def review_with_place(place_id):
    """Get all reviews"""
    place = get_by_id(Place, place_id, "dict")
    if place is None:
        abort(404)

    # Returns all review instances of the place
    if request.method == 'GET':
        reviews = [review.to_dict() for review in storage.all(Review).values()
                  if review.place_id == place_id]
        return jsonify(reviews)

    # Creates a new review instance with place relationship
    if request.method == "POST":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        if 'name' not in http_json:
            abort(400, description="Missing name")
        if "text" not in http_json:
            abort(400, description="Missing text")
        if 'user_id' not in http_json:
            abort(400, description="Missing user_id")
        user_check = get_by_id(User, http_json["user_id"], "obj")
        if user_check is None:
            abort(404)
        new_review = Review(**http_json)
        setattr(new_review, "place_id", place_id)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def reviews_with_id(review_id):
    """Get one specific review object by id"""
    # Check if there is a review with given id
    review = get_by_id(Review, review_id, "dict")
    if review is None:
        abort(404)

    # Return the review with code 200
    if request.method == 'GET':
        return jsonify(review), 200

    # Delete the review and save with code 200
    elif request.method == "DELETE":
        all_reviews = storage.all(Review)
        review = all_reviews.get('Review.' + review_id)
        if review:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    # Update the review with given attributes
    elif request.method == 'PUT':
        review = get_by_id(Review, review_id, "obj")
        if review is None:
            abort(404)
        if request.is_json:
            review_data = request.get_json()
        else:
            abort(400, description="Not a JSON")
        for key, val in review_data.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id', 'place_id']:
                setattr(review[0], key, val)
        storage.save()
        return jsonify(review[0].to_dict()), 200


def get_by_id(cls, id, switch):
    """Function to get object by id"""
    if switch == "dict":
        obj = [obj.to_dict() for obj in storage.all(cls).values()
               if obj.id == id]
        return obj[0] if obj else None
    if switch == "obj":
        obj = [obj for obj in storage.all(cls).values()
               if obj.id == id]
        return obj if obj else None
