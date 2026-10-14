
"""A party joins the list; impossible and malformed requests
are refused differently.
"""

from fastapi.testclient import TestClient

from tableturn.app import app


def test_invalid_party_size_returns_validation_error():
    client = TestClient(app)

    response = client.post(
        "/waitlist",
        json={"name": "Rao", "covers": 0},
    )

    assert response.status_code == 422
    assert response.json()["type"] == "/errors/validation"


def test_impossible_party_size_returns_party_too_big():
    client = TestClient(app)

    response = client.post(
        "/waitlist",
        json={"name": "Rao", "covers": 9},
    )

    assert response.status_code == 400
    assert response.json()["type"] == "/errors/party-too-big"
