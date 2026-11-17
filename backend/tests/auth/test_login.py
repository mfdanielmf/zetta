from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.exceptions import (
    ContraseñaIncorrectaException,
    UsuarioNoEncontradoException,
)

client = TestClient(app)


def test_login_usuario_no_existente():
    data = {
        "nombre": "noseee",
        "contraseña": "algo"
    }

    with patch("app.routes.auth_routes.login_usuario") as mock_login:
        mock_login.side_effect = UsuarioNoEncontradoException(
            "Usuario no encontrado")
        response = client.post("/auth/login", json=data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Credenciales incorrectas"}


def test_login_contraseña_incorrecta():
    data = {
        "nombre": "noseeeeee",
        "contraseña": "algoooo"
    }

    with patch("app.routes.auth_routes.login_usuario") as mock_login:
        mock_login.side_effect = ContraseñaIncorrectaException(
            "La contraseña es incorrecta")
        response = client.post("/auth/login", json=data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Credenciales incorrectas"}
