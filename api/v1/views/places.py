#!/usr/bin/python3
"""
Module to handle the place class routes
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_with_city(city_id):
    """Get all places"""
    city = get_by_id(City, city_id, "dict")
    if city is None:
        abort(404)

    # Returns all place instances of the City
    if request.method == 'GET':
        places = [place.to_dict() for place in storage.all(Place).values()
                  if place.city_id == city_id]
        return jsonify(places)

    # Creates a new place instance with City relationship
    if request.method == "POST":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        if 'user_id' not in http_json:
            abort(400, description="Missing user_id")
        user_check = get_by_id(User, http_json["user_id"], "obj")
        if not user_check:
            abort(404)
        new_place = Place(**http_json)
        setattr(new_place, "city_id", city_id)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_with_id(place_id):
    """Get one specific place object by id"""
    # Check if there is a place with given id
    place = get_by_id(Place, place_id, "dict")
    if place is None:
        abort(404)

    # Return the place with code 200
    if request.method == 'GET':
        return jsonify(place), 200

    # Delete the place and save with code 200
    elif request.method == "DELETE":
        all_places = storage.all(Place)
        place = all_places.get('Place.' + place_id)
        if place:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    # Update the place with given attributes
    elif request.method == 'PUT':
        place = get_by_id(Place, place_id, "obj")
        if place is None:
            abort(404)
        if request.is_json:
            place_data = request.get_json()
        else:
            abort(400, description="Not a JSON")
        for key, val in place_data.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id', 'city_id']:
                setattr(place[0], key, val)
        storage.save()
        return jsonify(place[0].to_dict()), 200


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
