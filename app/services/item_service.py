"""Business logic for laboratory items."""

from app.database import get_db
from app.repositories import item_repository
from app.validators import validate_item_payload


def list_items():
    """Return every item with its current stock."""
    return item_repository.get_all()


def add_item(payload):
    """Validate and store a new item.

    ``available_stock`` is initialized to ``total_stock`` by the repository.
    """
    name, total_stock = validate_item_payload(payload)
    db = get_db()
    try:
        item = item_repository.create(name, total_stock, db=db)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return item
