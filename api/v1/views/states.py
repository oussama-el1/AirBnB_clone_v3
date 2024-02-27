#!/usr/bin/python3
"""view for State Objects"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """Retrieves the list of all State objects:"""
    listObject = []
    for obj in storage.all(State).values():
        listObject.append(obj)
    return jsonify([obj.to_dict() for obj in listObject])


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """ handles GET method """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@app_views.route('/states/<state_id>',  methods=['DELETE'])
def delete_state(state_id):
    """delete a satate"""
    MatchingKey = "State" + "." + state_id
    for k, v in storage.all(State).items():
        if k == MatchingKey:
            storage.delete(v)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """Post state"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")
    obj = State(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updtdate_state(state_id):
    """Update state"""
    try:
        matchstring = 'State.' + state_id
        obj = storage.all(State)[matchstring]
    except Exception:
        obj = None
    if obj is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    for st in storage.all(State).values():
        if st.id == state_id:
            st.name = request.json['name']
    storage.save()
    return jsonify(obj.to_dict()), 200
