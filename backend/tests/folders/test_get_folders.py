from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.folder import Folder
from app.models.user import User
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user

client = TestClient(app=app)


def test_get_carpetas_sin_login():
    response = client.get("/api/folders")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "No se proporcionó token"
    }


def test_get_carpetas_usuario_sin_uploads():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/api/folders")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_get_carpetas_usuario_con_uploads():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    carpeta: Folder = Folder(
        id=uuid.uuid4(),
        nombre_original="testing",
        path=f"uploads/{usuario.id}/testing",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario
    )

    with patch("app.routes.folder_routes.obtener_carpetas_usuario_raiz") as mock_obtener:
        mock_obtener.return_value = [carpeta]

        response = client.get("/api/folders")

    assert response.status_code == 200
    json_response = response.json()

    assert len(json_response) == 1
    assert json_response[0]["nombre_original"] == carpeta.nombre_original
    assert json_response[0]["nombre_usuario"] == usuario.nombre

    app.dependency_overrides.clear()
