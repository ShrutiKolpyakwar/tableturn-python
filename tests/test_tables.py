from fastapi.testclient import TestClient

from tableturn.app import app


def test_floor_has_22_free_tables():
    with TestClient(app) as client:
        response = client.get("/branches/Baner/tables")

    assert response.status_code == 200

    data = response.json()
    assert len(data["tables"]) == 22
    assert data["free"] == 22
    assert all(table["state"] == "free" for table in data["tables"])


def test_second_startup_keeps_22_tables():
    with TestClient(app) as client:
        response = client.get("/branches/Baner/tables")
        assert response.status_code == 200
        assert len(response.json()["tables"]) == 22

    with TestClient(app) as client:
        response = client.get("/branches/Baner/tables")
        assert response.status_code == 200
        assert len(response.json()["tables"]) == 22
        assert response.json()["free"] == 22


def test_garden_filter():
    with TestClient(app) as client:
        response = client.get(
            "/branches/Baner/tables",
            params={"section": "Garden"},
        )

    assert response.status_code == 200
    data = response.json()

    assert len(data["tables"]) == 8
    assert data["free"] == 8
    assert all(t["section"] == "Garden" for t in data["tables"])


def test_unknown_branch_returns_404():
    with TestClient(app) as client:
        response = client.get("/branches/Aundh/tables")

    assert response.status_code == 404
    assert response.json()["type"] == "/errors/no-such-branch"


def test_unknown_table_returns_404():
    with TestClient(app) as client:
        response = client.get("/branches/Baner/tables/T99")

    assert response.status_code == 404
    assert response.json()["type"] == "/errors/no-such-table"