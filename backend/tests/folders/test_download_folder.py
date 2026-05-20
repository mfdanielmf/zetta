import tempfile
from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import CarpetaNoEncontradaException
from app.models.folder import Folder
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user

client = TestClient(app=app)


# Integración
def test_descargar_carpeta_existente():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_carpeta = uuid.uuid4()

    carpeta_falsa = Folder(
        id=uuid.uuid4(),
        nombre_original="testing",
        path=f"uploads/{usuario.id}/testing",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario,
        favorito=False
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(b"PK\x03\x04fakezipcontent")
        tmp_path = tmp.name

    with patch("app.routes.folder_routes.folder_services.descargar_carpeta") as mock_descargar:
        mock_descargar.return_value = (tmp_path, carpeta_falsa)

        response = client.get(f"/api/folders/{id_carpeta}")

    assert response.status_code == 200
    assert "application/zip" in response.headers["content-type"]
    assert "testing.zip" in response.headers["content-disposition"]

    app.dependency_overrides.clear()


def test_descargar_carpeta_no_encontrada():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.folder_services.descargar_carpeta") as mock_guardar:
        mock_guardar.side_effect = CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

        response = client.get(f"/api/folders/{id_carpeta}")

    assert response.status_code == 404
    assert response.json()[
        "detail"] == f"No se ha encontrado la carpeta con id {id_carpeta}"

    app.dependency_overrides.clear()
