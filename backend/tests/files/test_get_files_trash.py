from unittest.mock import patch
import uuid
from app.main import app
from fastapi.testclient import TestClient
from app.models.file import File
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user

client = TestClient(app)


def test_get_archivos_papelera_vacia():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/api/files/trash?page=1&limit=25")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["items"] == []
    assert json_response["total"] == 0
    assert json_response["pagina"] == 1
    assert json_response["limite"] == 25

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
        usuario=usuario,
    )

    with patch("app.routes.file_routes.file_services.obtener_archivos_papelera_raiz_paginados") as mock_obtener:
        mock_obtener.return_value = (1, [archivo_fake])

        response = client.get("/api/files/trash?page=1&limit=25")

    assert response.status_code == 200
    json_response = response.json()

    assert "items" in json_response
    assert json_response["total"] == 1
    assert json_response["pagina"] == 1
    assert json_response["limite"] == 25

    assert len(json_response["items"]) == 1

    item = json_response["items"][0]
    assert item["nombre_original"] == archivo_fake.nombre_original
    assert item["nombre_usuario"] == usuario.nombre
    assert item["fecha_eliminacion"] == archivo_fake.fecha_eliminacion

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

    archivo_fake2 = File(
        id=uuid.uuid4(),
        nombre_original="test2.txt",
        tamaño_bytes=100,
        path="uploads/test2.txt",
        fecha_creacion="2026-01-22T01:44:31.825198",
        id_usuario=usuario.id,
        fecha_eliminacion="2026-02-15T10:00:00",
        usuario=usuario
    )

    archivos_falsos = [archivo_fake, archivo_fake2]

    with patch("app.routes.file_routes.file_services.obtener_archivos_papelera_raiz_paginados") as mock_obtener:
        mock_obtener.return_value = (2, archivos_falsos)

        response = client.get("/api/files/trash?page=1&limit=25")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["total"] == 2
    assert len(json_response["items"]) == 2
    assert json_response["pagina"] == 1
    assert json_response["limite"] == 25

    for i, archivo in enumerate(archivos_falsos):
        item = json_response["items"][i]

        assert item["id"] == str(archivo.id)
        assert item["nombre_original"] == archivo.nombre_original
        assert item["path"] == archivo.path
        assert item["id_usuario"] == str(archivo.id_usuario)
        assert item["nombre_usuario"] == usuario.nombre
        assert item["fecha_eliminacion"] == str(archivo.fecha_eliminacion)

    app.dependency_overrides.clear()
