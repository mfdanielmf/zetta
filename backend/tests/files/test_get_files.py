from unittest.mock import patch
import uuid
from app.main import app
from fastapi.testclient import TestClient
from app.models.file import File
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user

client = TestClient(app)


def test_get_archivos_sin_login():
    response = client.get("/api/files")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "No se proporcionó token"
    }


def test_get_archivos_usuario_sin_uploads():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/api/files")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_get_archivos_usuario_con_uploads():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    archivo_fake = File(
        id=uuid.uuid4(),
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario
    )

    with patch("app.routes.file_routes.obtener_archivos_usuario") as mock_obtener:
        mock_obtener.return_value = [archivo_fake]

        response = client.get("/api/files")

    assert response.status_code == 200
    json_response = response.json()

    assert len(json_response) == 1
    assert json_response[0]["nombre_original"] == "testing.txt"
    assert json_response[0]["nombre_usuario"] == usuario.nombre

    app.dependency_overrides.clear()
