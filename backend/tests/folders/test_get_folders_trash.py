from unittest.mock import patch
import uuid
from app.main import app
from fastapi.testclient import TestClient
from app.models.folder import Folder
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user

client = TestClient(app)


def test_get_carpetas_papelera_vacia():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/api/folders/trash?page=1&limit=25")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["items"] == []
    assert json_response["total"] == 0

    app.dependency_overrides.clear()


def test_get_papelera_1_carpeta():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    carpeta: Folder = Folder(
        id=uuid.uuid4(),
        nombre_original="testing",
        path=f"uploads/{usuario.id}/testing",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        fecha_eliminacion="2026-02-15T10:00:00",
        usuario=usuario
    )

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_papelera_raiz_paginadas") as mock_obtener:
        mock_obtener.return_value = (1, [carpeta])

        response = client.get("/api/folders/trash?page=1&limit=25")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["total"] == 1
    assert len(json_response["items"]) == 1

    item = json_response["items"][0]

    assert item["nombre_original"] == carpeta.nombre_original
    assert item["nombre_usuario"] == usuario.nombre
    assert item["fecha_eliminacion"] == carpeta.fecha_eliminacion
    assert item["path"] == carpeta.path

    app.dependency_overrides.clear()


def test_get_papelera_varias_carpetas():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    carpeta: Folder = Folder(
        id=uuid.uuid4(),
        nombre_original="testing",
        path=f"uploads/{usuario.id}/testing",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        fecha_eliminacion="2026-02-15T10:00:00",
        usuario=usuario
    )

    carpeta2: Folder = Folder(
        id=uuid.uuid4(),
        nombre_original="testing2",
        path=f"uploads/{usuario.id}/testing2",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        fecha_eliminacion="2026-02-15T10:00:00",
        usuario=usuario
    )

    carpetas_falsas: list[Folder] = [carpeta, carpeta2]

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_papelera_raiz_paginadas") as mock_obtener:
        mock_obtener.return_value = (2, carpetas_falsas)

        response = client.get("/api/folders/trash?page=1&limit=25")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["total"] == 2
    assert len(json_response["items"]) == 2

    for i, carpeta in enumerate(carpetas_falsas):
        item = json_response["items"][i]

        assert item["id"] == str(carpeta.id)
        assert item["nombre_original"] == carpeta.nombre_original
        assert item["path"] == carpeta.path
        assert item["id_usuario"] == str(carpeta.id_usuario)
        assert item["nombre_usuario"] == usuario.nombre
        assert item["fecha_eliminacion"] == carpeta.fecha_eliminacion

    app.dependency_overrides.clear()
