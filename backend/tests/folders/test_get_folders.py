from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.folder import Folder
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
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

    response = client.get("/api/folders?page=1&limit=25")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["items"] == []
    assert json_response["total"] == 0

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
        usuario=usuario,
        favorito=False
    )

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_usuario_raiz_paginadas") as mock_obtener:
        mock_obtener.return_value = (1, [carpeta])

        response = client.get("/api/folders?page=1&limit=25")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["total"] == 1
    assert len(json_response["items"]) == 1

    item = json_response["items"][0]

    assert item["nombre_original"] == carpeta.nombre_original
    assert item["nombre_usuario"] == usuario.nombre

    app.dependency_overrides.clear()
