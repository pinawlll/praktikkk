"""Data access for the Item entity."""

from app.database import get_db


def create(name, total_stock, db=None):
    """Insert a new item and return it.

    A new item starts with ``available_stock`` equal to ``total_stock``.
    The caller is responsible for committing the transaction.
    """
    db = db or get_db()
    cursor = db.execute(
        "INSERT INTO item (name, total_stock, available_stock) VALUES (?, ?, ?)",
        (name, total_stock, total_stock),
    )
    return get_by_id(cursor.lastrowid, db=db)


def get_all(db=None):
    """Return every item ordered by id."""
    db = db or get_db()
    rows = db.execute(
        "SELECT id, name, total_stock, available_stock FROM item ORDER BY id"
    ).fetchall()
    return [dict(row) for row in rows]


def get_by_id(item_id, db=None):
    """Return a single item as a dict, or ``None`` when it does not exist."""
    db = db or get_db()
    row = db.execute(
        "SELECT id, name, total_stock, available_stock FROM item WHERE id = ?",
        (item_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def decrease_available_stock(item_id, quantity, db=None):
    """Reduce available stock only when the stock is sufficient.

    Returns ``True`` when a row was updated and ``False`` when the item does
    not exist or does not have enough stock.
    """
    db = db or get_db()
    cursor = db.execute(
        "UPDATE item SET available_stock = available_stock - ? "
        "WHERE id = ? AND available_stock >= ?",
        (quantity, item_id, quantity),
    )
    return cursor.rowcount == 1


def increase_available_stock(item_id, quantity, db=None):
    """Restore available stock and return ``True`` when a row was updated."""
    db = db or get_db()
    cursor = db.execute(
        "UPDATE item SET available_stock = available_stock + ? WHERE id = ?",
        (quantity, item_id),
    )
    return cursor.rowcount == 1
