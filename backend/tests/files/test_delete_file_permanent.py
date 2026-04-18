import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.auth_services import get_current_user
from app.models.exceptions import ArchivoNoEncontradoException, EliminarDiscoException
from tests.util import override_get_current_user

client = TestClient(app)


def test_eliminar_archivo_permanente_success():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_archivo: uuid.UUID = uuid.uuid4()

    with patch("app.routes.file_routes.eliminar_archivo_permanente") as mock_delete:
        mock_delete.return_value = None

        response = client.delete(f"/api/files/trash/{id_archivo}")

    assert response.status_code == 200
    assert response.json() == {
        "msg": "Archivo eliminado correctamente"
    }

    app.dependency_overrides.clear()


def test_eliminar_archivo_permanente_no_existente():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id_archivo: uuid.UUID = uuid.uuid4()

    with patch("app.routes.file_routes.eliminar_archivo_permanente") as mock_delete:
        mock_delete.side_effect = ArchivoNoEncontradoException()

        response = client.delete(f"/api/files/trash/{id_archivo}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No se ha encontrado el archivo en la papelera"
    }

    app.dependency_overrides.clear()


def test_eliminar_archivo_permanente_error_disco():
    app.dependency_overrides[get_current_user] = override_get_current_user

    archivo_id: uuid.UUID = uuid.uuid4()

    with patch("app.routes.file_routes.eliminar_archivo_permanente") as mock_delete:
        mock_delete.side_effect = EliminarDiscoException(
            "Error al eliminar el archivo del disco")

        response = client.delete(f"/api/files/trash/{archivo_id}")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Error al eliminar el archivo del disco"
    }

    app.dependency_overrides.clear()
