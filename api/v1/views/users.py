#!/usr/bin/python3
"""view for User Objects"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_user():
    """Retrieves the list of all User objects:"""
    listObject = []
    for obj in storage.all(User).values():
        listObject.append(obj)
    return jsonify([obj.to_dict() for obj in listObject])


@app_views.route('/users/<user_id>', methods=['GET'])
def user_get(user_id):
    """ handles GET method """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',  methods=['DELETE'])
def delete_user(user_id):
    """delete a user"""
    MatchingKey = "User" + "." + user_id
    for k, v in storage.all(User).items():
        if k == MatchingKey:
            storage.delete(v)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Post User"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    obj = User(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update city"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignored_keys:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
