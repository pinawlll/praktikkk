"""Stock consistency across several borrowing and returning transactions."""


def add_item(client, total_stock=10):
    response = client.post(
        "/items", json={"name": "Multimeter", "total_stock": total_stock}
    )
    return response.get_json()


def borrow(client, item_id, quantity):
    response = client.post(
        "/loans",
        json={"student_id": "20240001", "item_id": item_id, "quantity": quantity},
    )
    assert response.status_code == 201
    return response.get_json()


def return_loan(client, loan_id):
    response = client.put(f"/loans/{loan_id}/return")
    assert response.status_code == 200
    return response.get_json()


def item_stock(client, item_id):
    items = client.get("/items").get_json()["items"]
    return next(item for item in items if item["id"] == item_id)


def active_borrowed_quantity(client):
    loans = client.get("/loans/student/20240001").get_json()["loans"]
    return sum(loan["quantity"] for loan in loans if loan["status"] == "BORROWED")


def assert_stock_invariant(client, item_id, total_stock):
    item = item_stock(client, item_id)
    assert item["available_stock"] == total_stock - active_borrowed_quantity(client)
    assert 0 <= item["available_stock"] <= item["total_stock"]


def test_stock_stays_consistent_after_multiple_transactions(client):
    total_stock = 10
    item = add_item(client, total_stock=total_stock)

    first = borrow(client, item["id"], 3)
    assert item_stock(client, item["id"])["available_stock"] == 7
    assert_stock_invariant(client, item["id"], total_stock)

    second = borrow(client, item["id"], 2)
    assert item_stock(client, item["id"])["available_stock"] == 5
    assert_stock_invariant(client, item["id"], total_stock)

    return_loan(client, first["id"])
    assert item_stock(client, item["id"])["available_stock"] == 8
    assert_stock_invariant(client, item["id"], total_stock)

    third = borrow(client, item["id"], 4)
    assert item_stock(client, item["id"])["available_stock"] == 4
    assert_stock_invariant(client, item["id"], total_stock)

    return_loan(client, second["id"])
    assert item_stock(client, item["id"])["available_stock"] == 6
    assert_stock_invariant(client, item["id"], total_stock)

    return_loan(client, third["id"])
    assert item_stock(client, item["id"])["available_stock"] == total_stock
    assert active_borrowed_quantity(client) == 0
    assert_stock_invariant(client, item["id"], total_stock)
