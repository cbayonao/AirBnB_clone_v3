#!/usr/bin/python3
"""
Status of your API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def handler_close(self):
    """
    Handle close session from SQLAlchemy
    """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """
    Handles 404 errors
    """
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True, debug=True)
