#!/usr/bin/python3
"""
Module to handle the User class routes
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def users():
    """Get all users"""

    # Returns all User instances
    if request.method == 'GET':
        users = [user.to_dict()
                     for user in storage.all(User).values()]
        return jsonify(users)

    # Creates a new user
    if request.method == "POST":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        if 'name' not in http_json:
            abort(400, description="Missing name")
        new_user = User(**http_json)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id):
    """Get one specific user object by id"""
    # Check if there is a user with given id
    user = get_by_id(User, user_id, "dict")
    if user is None:
        abort(404)

    # Return the user with code 200
    if request.method == 'GET':
        return jsonify(user), 200

    # Delete the user and save with code 200
    elif request.method == "DELETE":
        all_users = storage.all(User)
        user = all_users.get('User.' + user_id)
        if user:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    # Update the user with given attributes
    elif request.method == 'PUT':
        user = get_by_id(User, user_id, "obj")
        if user is None:
            abort(404)
        if request.is_json:
            user_data = request.get_json()
        else:
            abort(400, description="Not a JSON")
        for key, val in user_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(user[0], key, val)
        storage.save()
        return jsonify(user[0].to_dict()), 200


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
