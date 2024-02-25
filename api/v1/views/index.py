#!/usr/bin/python3
"""import app_views bleuprint and create root"""
from api.v1.views import app_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status_ok():
    """status ok"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def count_objects():
    """count objects by types"""
    data = {
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    }
    return jsonify(data)
