from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_me_sin_token():
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "No se proporcionó token"
    }


def test_me_token_incorrecto():
    response = client.get("/auth/me", headers={"Authorization": "Bearer test"})

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Token incorrecto o expirado"
    }
