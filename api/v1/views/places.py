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
        if 'name' not in http_json:
            abort(400, description="Missing name")
        if 'user_id' not in http_json:
            abort(400, description="Missing user_id")
        user_check = get_by_id(User, http_json["user_id"], "obj")
        if user_check is None:
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

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    from models.state import State
    from models.city import City
    from models.amenity import Amenity

    request_json = request.get_json() # Get JSON from request
    if request_json is None:
        return jsonify({"error": "Not a JSON"}), 400
    states = request_json.get('states', []) # List of state ids
    cities = request_json.get('cities', []) # List of city ids
    amenities = request_json.get('amenities', []) # List of amenity ids

    # Create list of city objects from states in request
    if len(states) != 0:
        states_cities_obj_list = []
        for state_id in states: # For each state id in states list
            for city in storage.get(State, state_id).cities: # For each city in states cities list
                states_cities_obj_list.append(city) # Add city object to list

    # Create list of city objects from cities in request
    if len(cities) != 0:
        cities_obj_list = [storage.get(City, city_id) for city_id in cities]

    # Combine both city lists and remove cities with matching ids
    if len(states_cities_obj_list) > 0 and len(cities_obj_list) > 0:
        all_city_objs = list({city.id: city for city in states_cities_obj_list + cities_obj_list}.values())
    elif len(states_cities_obj_list) > 0:
        all_city_objs = states_cities_obj_list
    elif len(cities_obj_list) > 0:
        all_city_objs = cities_obj_list

    # Create a list of all places from filtered cities
    places_objs = [place for city in all_city_objs for place in city.places]

    # Create a list of amenity objects from amenity ids
    if len(amenities) != 0:
        amenities_objs = [storage.get(Amenity, amenity_id) for amenity_id in amenities]
        # Set places_objs to only places with ALL amenities
        places_objs = [place for place in places_objs if all(amenity in place.amenities for amenity in amenities_objs)]

    # Get the user name from the user_id in each place
    for place in places_objs:
        user_obj = storage.get(User, place.user_id)
        place.user = user_obj.first_name + " " + user_obj.last_name

    # Make list serializable
    places_objs = [place.to_dict() for place in places_objs]
    if len(amenities) != 0:
        for place in places_objs: # Change amenities to list of dicts instead of objects
            place['amenities'] = [amenity.to_dict() for amenity in place['amenities']]
    return jsonify(places_objs), 200

