#!/usr/bin/python3
"""
Module to contain routes
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status_json():
    """Return the status 'OK' if working"""
    status = {}
    status["status"] = "OK"
    return status

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_class_counts():
    """Returns the counts of each classes instances"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models.__init__ import storage

    classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}
    dict = {obj: storage.count(classes[obj]) for obj in classes}
    return jsonify(dict)
