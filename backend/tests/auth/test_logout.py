from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_logout():
    response = client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json() == {
        "msg": "Sesión cerrada con éxito"
    }
