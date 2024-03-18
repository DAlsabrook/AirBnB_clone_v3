#!/usr/bin/python3
"""
Module to handle the amenity class routes
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenity():
    """Get all amenities"""

    # Returns all amenity instances
    if request.method == 'GET':
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
        return jsonify(amenities)

    # Creates a new amenity
    if request.method == "POST":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        if 'name' not in http_json:
            abort(400, description="Missing name")
        new_amenity = Amenity(**http_json)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_with_id(amenity_id):
    """Get one specific amenity object by id"""
    # Check if there is a amenity with given id
    amenity = get_by_id(Amenity, amenity_id, "dict")
    if amenity is None:
        abort(404)

    # Return the amenity with code 200
    if request.method == 'GET':
        return jsonify(amenity), 200

    # Delete the amenity and save with code 200
    elif request.method == "DELETE":
        all_amenities = storage.all(Amenity)
        amenity = all_amenities.get('Amenity.' + amenity_id)
        if amenity:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    # Update the amenity with given attributes
    elif request.method == 'PUT':
        amenity = get_by_id(Amenity, amenity_id, "obj")
        if amenity is None:
            abort(404)
        if request.is_json:
            amenity_data = request.get_json()
        else:
            abort(400, description="Not a JSON")
        for key, val in amenity_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, val)
        storage.save()
        return jsonify(amenity.to_dict()), 200


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
