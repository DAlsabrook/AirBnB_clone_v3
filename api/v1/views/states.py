#!/usr/bin/python3
"""
Module to handle the state class routes
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/api/v1/states', methods=['GET'])
def all_states():
    """Get all states"""
    states = storage.all(State).values()
    dict_list = [state.to_dict() for state in states]
    return jsonify(dict_list)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def one_state(state_id):
    """Get one specific state object by id"""
    state = get_state_by_id(state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Removes a state from storage"""
    state = get_state_by_id(state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states', methods=['POST'])
def new_state():
    """Creates a new state object"""
    # Gets data from https and silent makes it return None if error instead
    # of raising an error
    http_json = request.get_json(silent=True)
    if http_json is None:
        abort(400, description="Not a JSON")
    if 'name' not in http_json:
        abort(400, description="Missing name")

    new_state = State(**http_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a current state object"""
    state = get_state_by_id(state_id)
    if state is None:
        abort(404)
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
