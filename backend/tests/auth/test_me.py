from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_me_sin_token():
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Usuario no autenticado"
    }


def test_me_token_incorrecto():
    response = client.get("/auth/me", cookies={"access_token": "wwww"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Token incorrecto"
    }
