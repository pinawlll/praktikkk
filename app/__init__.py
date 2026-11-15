"""Application factory for the Lab Equipment Loan System."""

import os

from flask import Flask

from . import database


def create_app(test_config=None):
    """Create and configure a Flask application instance."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # The SQLite database lives in the instance folder, outside version control.
        DATABASE=os.path.join(app.instance_path, "lab_equipment.db"),
        JSON_SORT_KEYS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    # Ensure the instance folder exists before the database file is created.
    os.makedirs(app.instance_path, exist_ok=True)

    database.init_app(app)

    return app
