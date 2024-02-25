#!/usr/bin/python3
"""import app_views bleuprint and create root"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_ok():
    """status ok"""
    return jsonify({"status": "OK"})
