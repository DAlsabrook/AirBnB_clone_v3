#!/usr/bin/python3
"""
Module to contain routes
"""
from api.v1.views import app_views


@app_views.route('/status')
def status_json():
    """Return the status 'OK' if working"""
    status = {}
    status["status"] = "OK"
    return status
