#!/usr/bin/python3
"""
Module to handle the state class routes
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Get all states"""
    # Returns all state instances
    if request.method == 'GET':
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)

    # Creates a new state instance
    if request.method == "POST":
        http_json = request.get_json(silent=True)
        if http_json is None:
            abort(400, description="Not a JSON")
        if 'name' not in http_json:
            abort(400, description="Missing name")
        new_state = State(**http_json)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states_with_id(state_id):
    """Get one specific state object by id"""
    # Check if there is a state with given id
    state = get_state_by_id(state_id)
    if state is None:
        abort(404)

    # Return the state with code 200
    if request.method == 'GET':
        return jsonify(state), 200

    # Delete the state and save with code 200
    elif request.method == "DELETE":
        all_states = storage.all(State)
        state = all_states.get('State.' + state_id)
        if state:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    # Update the state with given attributes
    elif request.method == 'PUT':
        state = get_state_by_id(state_id)
        if state is None:
            abort(404)
        if request.is_json:
            state_data = request.get_json()
        else:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, val in state_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                state[key] = val
        storage.save()
        return jsonify(state), 200


def get_state_by_id(state_id):
    """Function to get state by id"""
    state_obj = [state.to_dict() for state in storage.all(State).values()
                 if state.id == state_id]
    return state_obj[0] if state_obj else None
