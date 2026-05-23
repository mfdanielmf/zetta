import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.models.file import File
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.models.exceptions import ArchivoNoEncontradoException, ArchivoPapeleraException
from tests.util import override_get_current_user

client = TestClient(app)


def test_añadir_archivo_papelera_success():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    archivo = File(
        id=uuid.uuid4(),
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario
    )

    with patch("app.routes.file_routes.file_services.añadir_archivo_papelera") as mock_añadir:
        mock_añadir.return_value = archivo

        response = client.delete(f"/api/files/{archivo.id}")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["msg"] == "Archivo enviado a la papelera con éxito"
    assert json_response["archivo"]["id"] == str(archivo.id)
    assert json_response["archivo"]["nombre_original"] == archivo.nombre_original
    assert json_response["archivo"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_añadir_papelera_archivo_no_encontrado():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.file_routes.file_services.añadir_archivo_papelera") as mock_añadir:
        mock_añadir.side_effect = ArchivoNoEncontradoException()

        response = client.delete(f"/api/files/{id_test}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"No se ha encontrado el archivo con ID {id_test}"
    }

    app.dependency_overrides.clear()


def test_añadir_papelera_archivo_que_ya_estaba():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.file_routes.file_services.añadir_archivo_papelera") as mock_añadir:
        mock_añadir.side_effect = ArchivoPapeleraException()

        response = client.delete(f"/api/files/{id_test}")

    assert response.status_code == 409
    assert response.json() == {
        "detail": "El archivo seleccionado ya está en la papelera"
    }

    app.dependency_overrides.clear()
