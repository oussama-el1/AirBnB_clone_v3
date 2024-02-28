#!/usr/bin/python3
""" view for place """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_place(city_id):
    """all places for city"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        return jsonify([place.to_dict() for place in obj.places]), 200


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ handles GET methode for one place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',  methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """add place to city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data.keys():
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data.keys():
        abort(400, 'Missing name')
    NewObj = Place(**data)
    NewObj.city_id = city_id
    NewObj.save()
    return jsonify(NewObj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignored_keys:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
