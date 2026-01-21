import uuid
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

from app.models.user import User
from app.models.exceptions import NombreYaUsadoException, CorreoYaUsadoException


client = TestClient(app)


def test_insertar_usuario():
    data = {
        "nombre": "testing",
        "correo": "testing@example.com",
        "contraseña": "testing",
        "contraseña_repetir": "testing"
    }

    mock_usuario = User(
        id=uuid.UUID("12345678-1234-5678-1234-567812345678"), nombre=data["nombre"], correo=data["correo"], contraseña=data["contraseña"], fecha_creacion="2026-01-21T01:44:31.825198")

    with patch("app.routes.auth_routes.crear_usuario") as mock_crear_usuario:
        mock_crear_usuario.return_value = mock_usuario
        response = client.post("/auth/register", json=data)

    assert response.status_code == 200
    assert response.json() == {
        "msg": "Usuario creado con exito",
        "usuario": {
            "id": "12345678-1234-5678-1234-567812345678",
            "nombre": "testing",
            "correo": "testing@example.com",
            "fecha_creacion": "2026-01-21T01:44:31.825198"
        }
    }


def test_insertar_usuario_nombre_usado():
    data = {
        "nombre": "testing",
        "correo": "testing@example.com",
        "contraseña": "testing",
        "contraseña_repetir": "testing"
    }

    with patch("app.routes.auth_routes.crear_usuario") as mock_crear_usuario:
        mock_crear_usuario.side_effect = NombreYaUsadoException(
            f"Ya se ha encontrado un usuario con nombre {data['nombre']}")
        response = client.post("/auth/register", json=data)

    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Ya se ha encontrado un usuario con nombre {data['nombre']}"}


def test_insertar_usuario_correo_usado():
    data = {
        "nombre": "testing",
        "correo": "testing@example.com",
        "contraseña": "testing",
        "contraseña_repetir": "testing"
    }

    with patch("app.routes.auth_routes.crear_usuario") as mock_crear_usuario:
        mock_crear_usuario.side_effect = CorreoYaUsadoException(
            f"Ya se ha encontrado un usuario con el correo {data['correo']}")
        response = client.post("/auth/register", json=data)

    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Ya se ha encontrado un usuario con el correo {data['correo']}"}
