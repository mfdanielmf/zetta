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

    response = client.get("/api/folders/trash")

    assert response.status_code == 200
    assert len(response.json()) == 0

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

    with patch("app.routes.folder_routes.obtener_carpetas_papelera_raiz") as mock_obtener:
        mock_obtener.return_value = [carpeta]

        response = client.get("/api/folders/trash")

    assert response.status_code == 200
    json_response = response.json()

    assert len(json_response) == 1
    assert json_response[0]["nombre_original"] == carpeta.nombre_original
    assert json_response[0]["nombre_usuario"] == usuario.nombre
    assert json_response[0]["fecha_eliminacion"] == carpeta.fecha_eliminacion
    assert json_response[0]["path"] == carpeta.path

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

    with patch("app.routes.folder_routes.obtener_carpetas_papelera_raiz") as mock_obtener:
        mock_obtener.return_value = carpetas_falsas

        response = client.get("/api/folders/trash")

    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 2

    assert response.status_code == 200
    for i, carpeta in enumerate(carpetas_falsas):
        assert json_response[i]["id"] == str(carpeta.id)
        assert json_response[i]["nombre_original"] == carpeta.nombre_original
        assert json_response[i]["path"] == carpeta.path
        assert json_response[i]["id_usuario"] == str(carpeta.id_usuario)
        assert json_response[i]["nombre_usuario"] == usuario.nombre
        assert json_response[i]["fecha_eliminacion"] == str(
            carpeta.fecha_eliminacion)

    app.dependency_overrides.clear()
