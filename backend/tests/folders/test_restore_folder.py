from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import CarpetaNoEncontradaException
from app.models.folder import Folder
from app.models.user import User
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user

client = TestClient(app=app)


def test_restaurar_carpeta():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    carpeta: Folder = Folder(
        id=uuid.uuid4(),
        nombre_original="testing.txt",
        path=f"uploads/{usuario.id}/testing",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario,
        fecha_eliminacion=None
    )

    with patch("app.routes.folder_routes.restaurar_carpeta_papelera") as mock_restaurar:
        mock_restaurar.return_value = carpeta

        response = client.put(f"/api/folders/{carpeta.id}/restaurar")

    assert response.status_code == 200
    json_response = response.json()
    carpeta_response = json_response["carpeta"]

    assert json_response["msg"] == "Carpeta restaurada correctamente"
    assert carpeta_response["id"] == str(carpeta.id)
    assert carpeta_response["nombre_original"] == carpeta.nombre_original
    assert carpeta_response["path"] == carpeta.path
    assert carpeta_response["id_usuario"] == str(carpeta.id_usuario)
    assert carpeta_response["fecha_eliminacion"] == None

    app.dependency_overrides.clear()


def test_restaurar_carpeta_id_no_encontrada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.file_routes.restaurar_archivo_papelera") as mock_restaurar:
        mock_restaurar.side_effect = CarpetaNoEncontradaException()

        response = client.put(f"/api/folders/{id_test}/restaurar")

    assert response.status_code == 404
    json_response = response.json()

    assert json_response[
        "detail"] == f"No se ha encontrado la carpeta con ID {id_test} en la papelera"

    app.dependency_overrides.clear()
