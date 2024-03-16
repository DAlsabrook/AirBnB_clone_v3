#!/usr/bin/python3
"""
Module for creating flask api
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

# Create an instance of Flask
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_errors(error):
    """Handle 404 page with dict"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(exception):
    """Call storage.close()"""
    storage.close()


if __name__ == "__main__":
    # Get host and port from environment variables with default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
