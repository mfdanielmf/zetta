from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import CarpetaNoEncontradaException
from app.models.file import File
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user

client = TestClient(app=app)


def test_obtener_archivos_carpeta():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_carpeta: uuid.UUID = uuid.uuid4()
    id_archivo: uuid.UUID = uuid.uuid4()

    archivo_falso: File = File(
        id=id_archivo,
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        id_carpeta=id_carpeta,
        usuario=usuario
    )

    with patch("app.routes.folder_routes.obtener_archivos_carpeta") as mock_obtener:
        mock_obtener.return_value = [archivo_falso]

        response = client.get(f"/api/folders/{id_carpeta}/files")

    assert response.status_code == 200
    json_response = response.json()[0]

    assert json_response["id"] == str(id_archivo)
    assert json_response["id_usuario"] == str(usuario.id)
    assert json_response["id_carpeta"] == str(id_carpeta)

    app.dependency_overrides.clear()


def test_obtener_archivos_carpeta_no_existente():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.obtener_archivos_carpeta") as mock_guardar:
        mock_guardar.side_effect = CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

        response = client.get(f"/api/folders/{id_carpeta}/files")

    assert response.status_code == 404
    assert response.json()[
        "detail"] == f"No se ha encontrado la carpeta con id {id_carpeta}"

    app.dependency_overrides.clear()


def test_obtener_archivos_carpeta_vacia():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.obtener_archivos_carpeta") as mock_guardar:
        mock_guardar.return_value = []

        response = client.get(f"/api/folders/{id_carpeta}/files")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()
