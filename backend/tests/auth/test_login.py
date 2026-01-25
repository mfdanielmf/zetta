from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from app.models.exceptions import UsuarioNoEncontradoException, ContraseñaIncorrectaException

client = TestClient(app)


def test_login_usuario_no_existente():
    data = {
        "nombre": "noseee",
        "contraseña": "algo"
    }

    with patch("app.routes.auth_routes.login_usuario") as mock_login:
        mock_login.side_effect = UsuarioNoEncontradoException(
            f"No se ha encontrado el usuario con nombre {data['nombre']}")
        response = client.post("/auth/login", json=data)

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"No se ha encontrado el usuario con nombre {data['nombre']}"}


def test_login_contraseña_incorrecta():
    data = {
        "nombre": "noseeeeee",
        "contraseña": "algoooo"
    }

    with patch("app.routes.auth_routes.login_usuario") as mock_login:
        mock_login.side_effect = ContraseñaIncorrectaException(
            "La contraseña es incorrecta")
        response = client.post("/auth/login", json=data)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "La contraseña es incorrecta"}
