"""Business logic for borrowing and returning items."""

from app.database import get_db
from app.errors import NotFoundError, ValidationError
from app.repositories import item_repository, loan_repository
from app.validators import validate_loan_payload


def borrow_item(payload):
    """Create a BORROWED loan and reduce stock in one transaction."""
    student_id, item_id, quantity = validate_loan_payload(payload)
    db = get_db()
    try:
        if item_repository.get_by_id(item_id, db=db) is None:
            raise NotFoundError("Item not found")

        # The conditional UPDATE prevents stock from going negative.
        if not item_repository.decrease_available_stock(item_id, quantity, db=db):
            raise ValidationError("Insufficient stock")

        loan = loan_repository.create(
            student_id, item_id, quantity, status="BORROWED", db=db
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    return loan


def return_item(loan_id):
    """Mark a loan as RETURNED and restore stock in one transaction."""
    db = get_db()
    try:
        loan = loan_repository.get_by_id(loan_id, db=db)
        if loan is None:
            raise NotFoundError("Loan not found")
        if loan["status"] == "RETURNED":
            raise ValidationError("Loan has already been returned")

        if not loan_repository.update_status(
            loan_id, "RETURNED", expected_status="BORROWED", db=db
        ):
            raise ValidationError("Loan has already been returned")

        item_repository.increase_available_stock(
            loan["item_id"], loan["quantity"], db=db
        )
        db.commit()
        loan = loan_repository.get_by_id(loan_id, db=db)
    except Exception:
        db.rollback()
        raise
    return loan


def get_student_history(student_id):
    """Return the loan history for a student."""
    return loan_repository.get_by_student_id(student_id)
