from unittest.mock import patch
import uuid
import io

from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import CarpetaNoEncontradaException
from app.models.folder import Folder
from app.models.user import User
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user

client = TestClient(app=app)


def test_descargar_carpeta_existente():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_carpeta: uuid.UUID = uuid.uuid4()

    buffer_falso = io.BytesIO()
    buffer_falso.write(b"PK\x03\x04fakezipcontent")
    buffer_falso.seek(0)

    carpeta_falsa: Folder = Folder(
        id=uuid.uuid4(),
        nombre_original="testing",
        path=f"uploads/{usuario.id}/testing",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario
    )

    with patch("app.routes.folder_routes.descargar_carpeta") as mock_descargar:
        mock_descargar.return_value = (buffer_falso, carpeta_falsa)

        response = client.get(f"/api/folders/{id_carpeta}")

    assert response.status_code == 200

    assert "application/zip" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
    assert "testing.zip" in response.headers["content-disposition"]

    assert response.content.startswith(b"PK")

    app.dependency_overrides.clear()


def test_descargar_carpeta_no_encontrada():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.descargar_carpeta") as mock_guardar:
        mock_guardar.side_effect = CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

        response = client.get(f"/api/folders/{id_carpeta}")

    assert response.status_code == 404
    assert response.json()[
        "detail"] == f"No se ha encontrado la carpeta con id {id_carpeta}"

    app.dependency_overrides.clear()
