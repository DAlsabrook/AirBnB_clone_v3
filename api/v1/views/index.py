#!/usr/bin/python3
"""
Module to contain routes
"""
from api.v1.views import app_views


@app_views.route('/status')
def status_json():
    """Return the status 'OK' if working"""
    status = {}
    status["status"] = "OK"
    return status

@app_views.route('/stats')
def get_class_counts():
    """Returns the counts of each classes instances"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models.__init__ import storage
    classes = {"Amenity": Amenity, "City": City,
               "Place": Place, "Review": Review,
                "State": State, "User": User}
    dict = {}
    for cls_str, cls in classes.items():
        dict[cls_str] = storage.count(cls)
    return dict
