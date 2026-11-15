"""Application factory for the Lab Equipment Loan System."""

import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from . import database
from .errors import ApiError
from .routes.item_routes import bp as items_bp
from .routes.loan_routes import bp as loans_bp


def create_app(test_config=None):
    """Create and configure a Flask application instance."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # The SQLite database lives in the instance folder, outside version control.
        DATABASE=os.path.join(app.instance_path, "lab_equipment.db"),
    )
    # Keep response keys in insertion order instead of alphabetical order.
    app.json.sort_keys = False

    if test_config is not None:
        app.config.update(test_config)

    # Ensure the instance folder exists before the database file is created.
    os.makedirs(app.instance_path, exist_ok=True)

    database.init_app(app)

    app.register_blueprint(items_bp)
    app.register_blueprint(loans_bp)

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({"error": error.description}), error.code

    return app
