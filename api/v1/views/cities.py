#!/usr/bin/python3
""" view for cities """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """all cities for state"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    else:
        return jsonify([city.to_dict() for city in obj.cities]), 200


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_get(city_id):
    """ handles GET methode for one City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>',  methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city(state_id):
    """add city to state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    city = request.get_json()
    if 'name' not in city:
        abort(400, 'Missing name')
    NewObj = City(**city)
    NewObj.state_id = state_id
    NewObj.save()
    return jsonify(NewObj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignored_keys:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
