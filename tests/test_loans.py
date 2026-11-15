"""Tests for the Loan, Return, and student history APIs."""

import pytest


def add_item(client, total_stock=10):
    response = client.post("/items", json={"name": "Multimeter", "total_stock": total_stock})
    return response.get_json()


def available_stock(client, item_id):
    items = client.get("/items").get_json()["items"]
    return next(item for item in items if item["id"] == item_id)["available_stock"]


def borrow(client, item_id, quantity, student_id="20240001"):
    return client.post(
        "/loans",
        json={"student_id": student_id, "item_id": item_id, "quantity": quantity},
    )


# 6.2 Loan API


def test_borrow_with_valid_data(client):
    item = add_item(client)

    response = borrow(client, item["id"], 3)

    assert response.status_code == 201
    loan = response.get_json()
    assert loan["student_id"] == "20240001"
    assert loan["item_id"] == item["id"]
    assert loan["quantity"] == 3
    assert loan["status"] == "BORROWED"


def test_borrow_when_stock_is_sufficient(client):
    item = add_item(client, total_stock=5)

    response = borrow(client, item["id"], 5)

    assert response.status_code == 201
    assert available_stock(client, item["id"]) == 0


def test_borrow_when_quantity_exceeds_stock(client):
    item = add_item(client, total_stock=3)

    response = borrow(client, item["id"], 4)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Insufficient stock"


def test_borrow_with_unknown_item(client):
    response = borrow(client, 9999, 1)

    assert response.status_code == 404
    assert "error" in response.get_json()


@pytest.mark.parametrize("quantity", [0, -1])
def test_borrow_with_non_positive_quantity(client, quantity):
    item = add_item(client)

    response = borrow(client, item["id"], quantity)

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_stock_decreases_by_borrowed_quantity(client):
    item = add_item(client, total_stock=10)

    borrow(client, item["id"], 3)

    assert available_stock(client, item["id"]) == 7


def test_failed_borrow_does_not_change_stock(client):
    item = add_item(client, total_stock=2)

    response = borrow(client, item["id"], 3)

    assert response.status_code == 400
    assert available_stock(client, item["id"]) == 2
    assert client.get("/loans/student/20240001").get_json() == {"loans": []}


# 6.3 Return API


def test_return_valid_loan(client):
    item = add_item(client)
    loan = borrow(client, item["id"], 4).get_json()

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 200


def test_return_changes_status_to_returned(client):
    item = add_item(client)
    loan = borrow(client, item["id"], 2).get_json()

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.get_json()["status"] == "RETURNED"
    history = client.get("/loans/student/20240001").get_json()["loans"]
    assert history[0]["status"] == "RETURNED"


def test_return_increases_stock_by_quantity(client):
    item = add_item(client, total_stock=10)
    loan = borrow(client, item["id"], 4).get_json()
    assert available_stock(client, item["id"]) == 6

    client.put(f"/loans/{loan['id']}/return")

    assert available_stock(client, item["id"]) == 10


def test_return_unknown_loan(client):
    response = client.put("/loans/9999/return")

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_return_already_returned_loan(client):
    item = add_item(client)
    loan = borrow(client, item["id"], 2).get_json()
    client.put(f"/loans/{loan['id']}/return")

    response = client.put(f"/loans/{loan['id']}/return")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_double_return_does_not_increase_stock(client):
    item = add_item(client, total_stock=10)
    loan = borrow(client, item["id"], 4).get_json()
    client.put(f"/loans/{loan['id']}/return")

    client.put(f"/loans/{loan['id']}/return")

    assert available_stock(client, item["id"]) == 10


# 6.4 Student Loan History API


def test_history_for_student_with_loans(client):
    item = add_item(client)
    borrow(client, item["id"], 2, student_id="20240001")
    borrow(client, item["id"], 1, student_id="20240001")

    response = client.get("/loans/student/20240001")

    assert response.status_code == 200
    loans = response.get_json()["loans"]
    assert len(loans) == 2
    assert all(loan["student_id"] == "20240001" for loan in loans)


def test_history_for_student_without_loans(client):
    response = client.get("/loans/student/00000000")

    assert response.status_code == 200
    assert response.get_json() == {"loans": []}


def test_history_only_contains_requested_student(client):
    item = add_item(client, total_stock=20)
    borrow(client, item["id"], 1, student_id="20240001")
    borrow(client, item["id"], 1, student_id="20249999")

    loans = client.get("/loans/student/20240001").get_json()["loans"]

    assert len(loans) == 1
    assert loans[0]["student_id"] == "20240001"
