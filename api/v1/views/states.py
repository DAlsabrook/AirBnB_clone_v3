#!/usr/bin/python3
"""
Module to handle the state class routes
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/api/v1/states', methods=['GET', 'POST'])
def states():
    """Get all states"""
    if request.method == 'GET':
        states = [state.to_dict() for state in storage.all("State").values()]
        return jsonify(states)
    if request.method == "POST":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        if 'name' not in http_json:
            abort(400, description="Missing name")

        new_state = State(**http_json)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states_with_id(state_id):
    """Get one specific state object by id"""
    state = get_state_by_id(state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return state
    elif request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        for key, value in http_json.items():
            if key not in ["id", "created_at", "updates_at"]:
                setattr(state, key, value)
                state.save()
        return jsonify(state.to_dict()), 200


def get_state_by_id(state_id):
    """Function to get state by id"""
    state_obj = [state for state in storage.all(State).values() if state.id == state_id]
    if not isinstance(state_obj, State):
        return None
    return state_obj
