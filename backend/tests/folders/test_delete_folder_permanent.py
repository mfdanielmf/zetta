import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.models.exceptions import CarpetaNoEncontradaException, EliminarDiscoException
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user

client = TestClient(app)


def test_eliminar_carpeta_permanente_success():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.eliminar_carpeta_permanente") as mock_delete:
        mock_delete.return_value = None

        response = client.delete(f"/api/folders/trash/{id_carpeta}")

    assert response.status_code == 200
    assert response.json() == {
        "msg": "Carpeta eliminada correctamente"
    }

    app.dependency_overrides.clear()


def test_eliminar_carpeta_permanente_no_existente():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.eliminar_carpeta_permanente") as mock_delete:
        mock_delete.side_effect = CarpetaNoEncontradaException()

        response = client.delete(f"/api/folders/trash/{id_carpeta}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No se ha encontrado la carpeta en la papelera"
    }

    app.dependency_overrides.clear()


def test_eliminar_carpeta_permanente_error_disco():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.eliminar_carpeta_permanente") as mock_delete:
        mock_delete.side_effect = EliminarDiscoException(
            "Error al eliminar la carpeta del disco")

        response = client.delete(f"/api/folders/trash/{id_carpeta}")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Error al eliminar la carpeta del disco"
    }

    app.dependency_overrides.clear()
