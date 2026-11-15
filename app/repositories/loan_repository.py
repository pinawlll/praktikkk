"""Data access for the Loan entity."""

from app.database import get_db


def create(student_id, item_id, quantity, status="BORROWED", db=None):
    """Insert a new loan transaction and return it.

    The caller is responsible for committing the transaction.
    """
    db = db or get_db()
    cursor = db.execute(
        "INSERT INTO loan (student_id, item_id, quantity, status) "
        "VALUES (?, ?, ?, ?)",
        (student_id, item_id, quantity, status),
    )
    return get_by_id(cursor.lastrowid, db=db)


def get_by_id(loan_id, db=None):
    """Return a single loan as a dict, or ``None`` when it does not exist."""
    db = db or get_db()
    row = db.execute(
        "SELECT id, student_id, item_id, quantity, status, created_at "
        "FROM loan WHERE id = ?",
        (loan_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def update_status(loan_id, status, db=None):
    """Change the status of a loan and return ``True`` when it was updated."""
    db = db or get_db()
    cursor = db.execute(
        "UPDATE loan SET status = ? WHERE id = ?",
        (status, loan_id),
    )
    return cursor.rowcount == 1


def get_by_student_id(student_id, db=None):
    """Return the loan history for a student, newest first."""
    db = db or get_db()
    rows = db.execute(
        "SELECT id, student_id, item_id, quantity, status, created_at "
        "FROM loan WHERE student_id = ? ORDER BY created_at DESC, id DESC",
        (student_id,),
    ).fetchall()
    return [dict(row) for row in rows]
