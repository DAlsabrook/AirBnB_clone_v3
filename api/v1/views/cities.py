#!/usr/bin/python3
"""
Module to handle the city class routes
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_with_state(state_id):
    """Get all cities"""
    state = get_by_id(State, state_id, "dict")
    if state is None:
        abort(404)

    # Returns all city instances of the state
    if request.method == 'GET':
        cities = [city.to_dict() for city in storage.all(City).values()
                  if city.state_id == state_id]
        return jsonify(cities)

    # Creates a new city instance with state relationship
    if request.method == "POST":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        if 'name' not in http_json:
            abort(400, description="Missing name")
        new_city = City(**http_json)
        setattr(new_city, "state_id", state_id)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_with_id(city_id):
    """Get one specific city object by id"""
    # Check if there is a city with given id
    city = get_by_id(City, city_id, "dict")
    if city is None:
        abort(404)

    # Return the city with code 200
    if request.method == 'GET':
        return jsonify(city), 200

    # Delete the city and save with code 200
    elif request.method == "DELETE":
        all_cities = storage.all(City)
        city = all_cities.get('City.' + city_id)
        if city:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    # Update the city with given attributes
    elif request.method == 'PUT':
        city = get_by_id(City, city_id, "obj")
        if city is None:
            abort(404)
        if request.is_json:
            City_data = request.get_json()
        else:
            abort(400, description="Not a JSON")
        for key, val in City_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(city[0], key, val)
        storage.save()
        return jsonify(city[0].to_dict()), 200


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
