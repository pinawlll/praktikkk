"""Tests for the Item API."""


def create_item(client, name="Multimeter", total_stock=10):
    return client.post("/items", json={"name": name, "total_stock": total_stock})


def test_get_items_when_database_is_empty(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.get_json() == {"items": []}


def test_create_item_with_valid_data(client):
    response = create_item(client)

    assert response.status_code == 201
    item = response.get_json()
    assert item["id"] == 1
    assert item["name"] == "Multimeter"
    assert item["total_stock"] == 10
    assert item["available_stock"] == 10


def test_create_item_without_name(client):
    response = client.post("/items", json={"total_stock": 5})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_item_with_negative_stock(client):
    response = create_item(client, total_stock=-1)

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_initial_available_stock_equals_total_stock(client):
    create_item(client, total_stock=7)

    response = client.get("/items")

    item = response.get_json()["items"][0]
    assert item["total_stock"] == 7
    assert item["available_stock"] == item["total_stock"]
