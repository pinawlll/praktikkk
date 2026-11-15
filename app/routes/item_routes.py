"""HTTP routes for laboratory items."""

from flask import Blueprint, jsonify, request

from app.services import item_service

bp = Blueprint("items", __name__)


@bp.get("/items")
def list_items():
    """Return every item with its current stock."""
    return jsonify({"items": item_service.list_items()}), 200


@bp.post("/items")
def create_item():
    """Add a new item to the catalog."""
    item = item_service.add_item(request.get_json(silent=True))
    return jsonify(item), 201
