#!/usr/bin/python3
"""Amenity view"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenity():
    """Retrieves the list of all amenity objects:"""
    listObject = []
    for obj in storage.all(Amenity).values():
        listObject.append(obj)
    return jsonify([obj.to_dict() for obj in listObject]), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_get(amenity_id):
    """ handles GET method """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',  methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """Post amenity"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")
    obj = Amenity(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignored_keys = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignored_keys:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
