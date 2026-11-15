"""HTTP routes for borrowing and returning items."""

from flask import Blueprint, jsonify, request

from app.services import loan_service

bp = Blueprint("loans", __name__)


@bp.post("/loans")
def create_loan():
    """Create a borrowing transaction."""
    loan = loan_service.borrow_item(request.get_json(silent=True))
    return jsonify(loan), 201


@bp.put("/loans/<int:loan_id>/return")
def return_loan(loan_id):
    """Return a borrowed item."""
    return jsonify(loan_service.return_item(loan_id)), 200


@bp.get("/loans/student/<student_id>")
def student_loan_history(student_id):
    """Return the loan history for a student."""
    return jsonify({"loans": loan_service.get_student_history(student_id)}), 200
