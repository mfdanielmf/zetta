from unittest.mock import patch
import uuid
from app.main import app
from fastapi.testclient import TestClient
from app.models.file import File
from app.middleware.auth_middleware import get_current_user
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

    response = client.get("/api/files?page=1&limit=25")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["items"] == []
    assert json_response["total"] == 0
    assert json_response["pagina"] == 1
    assert json_response["limite"] == 25

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
        usuario=usuario,
        favorito=False
    )

    with patch("app.routes.file_routes.file_services.obtener_archivos_usuario_paginados") as mock_obtener:
        mock_obtener.return_value = (1, [archivo_fake])

        response = client.get("/api/files?page=1&limit=25")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["total"] == 1
    assert len(json_response["items"]) == 1

    item = json_response["items"][0]

    assert item["nombre_original"] == "testing.txt"
    assert item["nombre_usuario"] == usuario.nombre

    app.dependency_overrides.clear()
