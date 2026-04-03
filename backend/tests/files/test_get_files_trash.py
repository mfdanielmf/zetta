from unittest.mock import patch
import uuid
from app.main import app
from fastapi.testclient import TestClient
from app.models.file import File
from app.models.user import User
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user

client = TestClient(app)


def test_get_archivos_papelera_vacia():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/api/files/trash")

    assert response.status_code == 200
    assert len(response.json()) == 0

    app.dependency_overrides.clear()


def test_get_archivo_papelera():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    archivo_fake = File(
        id=uuid.uuid4(),
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        fecha_eliminacion="2026-02-15T10:00:00",
        usuario=usuario
    )

    with patch("app.routes.file_routes.obtener_archivos_papelera_raiz") as mock_obtener:
        mock_obtener.return_value = [archivo_fake]

        response = client.get("/api/files/trash")

    assert response.status_code == 200
    json_response = response.json()

    assert len(json_response) == 1
    assert json_response[0]["nombre_original"] == archivo_fake.nombre_original
    assert json_response[0]["nombre_usuario"] == usuario.nombre
    assert json_response[0]["fecha_eliminacion"] == archivo_fake.fecha_eliminacion

    app.dependency_overrides.clear()


def test_get_archivos_multiples_papelera():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    archivo_fake = File(
        id=uuid.uuid4(),
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        fecha_eliminacion="2026-02-15T10:00:00",
        usuario=usuario
    )

    archivo_fake2: File = File(
        id=uuid.uuid4(),
        nombre_original="test2.txt",
        tamaño_bytes="100",
        path=f"uploads/test2.txt",
        fecha_creacion="2026-01-22T01:44:31.825198",
        id_usuario=usuario.id,
        fecha_eliminacion="2026-02-15T10:00:00",
        usuario=usuario
    )

    archivos_falsos = [archivo_fake, archivo_fake2]

    with patch("app.routes.file_routes.obtener_archivos_papelera_raiz") as mock_obtener:
        mock_obtener.return_value = archivos_falsos

        response = client.get("/api/files/trash")

    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 2

    assert response.status_code == 200
    for i, archivo in enumerate(archivos_falsos):
        assert json_response[i]["id"] == str(archivo.id)
        assert json_response[i]["nombre_original"] == archivo.nombre_original
        assert json_response[i]["path"] == archivo.path
        assert json_response[i]["id_usuario"] == str(archivo.id_usuario)
        assert json_response[i]["nombre_usuario"] == usuario.nombre
        assert json_response[i]["fecha_eliminacion"] == str(
            archivo.fecha_eliminacion)

    app.dependency_overrides.clear()
