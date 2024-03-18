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

@app_views.route('/stats', methods=['GET'])
def get_class_counts():
    """Returns the counts of each classes instances"""
    from models.__init__ import storage
    return jsonify({
                    "amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
