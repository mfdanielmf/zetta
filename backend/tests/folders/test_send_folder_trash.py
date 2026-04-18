from unittest.mock import patch
from datetime import datetime
import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import CarpetaNoEncontradaException, CarpetaPapeleraException
from app.models.folder import Folder
from app.models.user import User
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user

client = TestClient(app=app)


def test_añadir_carpeta_papelera_success():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    carpeta = Folder(
        id=uuid.uuid4(),
        nombre_original="testing.txt",
        path=f"uploads/{usuario.id}/testing",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario,
        fecha_eliminacion=datetime.now()
    )

    with patch("app.routes.folder_routes.añadir_carpeta_papelera") as mock_añadir:
        mock_añadir.return_value = carpeta

        response = client.delete(f"/api/folders/{carpeta.id}")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["msg"] == "Carpeta enviada a la papelera con éxito"
    assert json_response["carpeta"]["id"] == str(carpeta.id)
    assert json_response["carpeta"]["nombre_original"] == carpeta.nombre_original
    assert json_response["carpeta"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_añadir_papelera_carpeta_no_encontrada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.añadir_carpeta_papelera") as mock_añadir:
        mock_añadir.side_effect = CarpetaNoEncontradaException()

        response = client.delete(f"/api/folders/{id_test}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"No se ha encontrado la carpeta con ID {id_test}"
    }

    app.dependency_overrides.clear()


def test_añadir_papelera_carpeta_que_ya_estaba():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.añadir_carpeta_papelera") as mock_añadir:
        mock_añadir.side_effect = CarpetaPapeleraException()

        response = client.delete(f"/api/folders/{id_test}")

    assert response.status_code == 409
    assert response.json() == {
        "detail": "La carpeta seleccionada ya está en la papelera"
    }

    app.dependency_overrides.clear()
