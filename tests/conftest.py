"""Shared pytest fixtures for the API tests."""

import pytest

from app import create_app
from app.database import init_db


@pytest.fixture
def app(tmp_path):
    """Create an application backed by a temporary database."""
    application = create_app(
        {"TESTING": True, "DATABASE": str(tmp_path / "test.db")}
    )
    with application.app_context():
        init_db()
    yield application


@pytest.fixture
def client(app):
    """Return a test client for the application."""
    return app.test_client()
