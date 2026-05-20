from unittest.mock import patch
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import ArchivoNoEncontradoException
from app.models.file import File
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user


client = TestClient(app)


def test_restaurar_archivo():
    usuario: User = override_get_current_user()
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

    with patch("app.routes.file_routes.file_services.restaurar_archivo_papelera") as mock_restaurar:
        mock_restaurar.return_value = archivo_fake

        response = client.put(f"/api/files/{archivo_fake.id}/restaurar")

    assert response.status_code == 200
    json_response = response.json()
    archivo_response = json_response["archivo"]

    assert json_response["msg"] == "Archivo restaurado correctamente"
    assert archivo_response["id"] == str(archivo_fake.id)
    assert archivo_response["nombre_original"] == archivo_fake.nombre_original
    assert archivo_response["path"] == archivo_fake.path
    assert archivo_response["id_usuario"] == str(archivo_fake.id_usuario)
    assert archivo_response["fecha_eliminacion"] == None

    app.dependency_overrides.clear()


def test_restaurar_archivo_id_no_encontrada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.file_routes.file_services.restaurar_archivo_papelera") as mock_restaurar:
        mock_restaurar.side_effect = ArchivoNoEncontradoException()

        response = client.put(f"/api/files/{id_test}/restaurar")

    assert response.status_code == 404
    json_response = response.json()

    assert json_response[
        "detail"] == f"No se ha encontrado el archivo con ID {id_test} en la papelera"

    app.dependency_overrides.clear()
