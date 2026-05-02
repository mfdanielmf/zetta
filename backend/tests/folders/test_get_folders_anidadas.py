import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import CarpetaNoEncontradaException
from app.models.folder import Folder
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user
from unittest.mock import patch
from app.config import config

client = TestClient(app=app)


def test_get_anidadas_carpeta_no_existente():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_dentro_carpeta") as mock_obtener:
        mock_obtener.side_effect = CarpetaNoEncontradaException()

        response = client.get(f"/api/folders/{id_carpeta}/folders")

    assert response.status_code == 404
    assert response.json()[
        "detail"] == f"No se ha encontrado la carpeta con id {id_carpeta}"

    app.dependency_overrides.clear()


def test_get_anidadas_sin_carpetas():
    app.dependency_overrides[get_current_user] = override_get_current_user

    random_id: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_dentro_carpeta") as mock_obtener:
        mock_obtener.return_value = []

        response = client.get(f"/api/folders/{random_id}/folders")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_get_anidadas_con_una_carpeta():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()
    random_id: uuid.UUID = uuid.uuid4()
    nombre_carpeta: str = "testing.txt"

    carpeta_falsa: Folder = Folder(
        id=id_test,
        nombre_original=nombre_carpeta,
        path=f"{config.UPLOAD_DIR}/{usuario.id}/{id_test}",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=usuario.id,
        usuario=usuario,
        id_carpeta=random_id
    )

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_dentro_carpeta") as mock_obtener:
        mock_obtener.return_value = [carpeta_falsa]

        response = client.get(f"/api/folders/{random_id}/folders")

    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response) == 1
    assert json_response[0]["nombre_original"] == nombre_carpeta
    assert json_response[0]["nombre_usuario"] == usuario.nombre
    assert json_response[0]["id_carpeta"] == str(random_id)

    app.dependency_overrides.clear()


def test_get_anidadas_con_varias_carpetas():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()
    id_test2: uuid.UUID = uuid.uuid4()
    random_id: uuid.UUID = uuid.uuid4()
    nombre_carpeta: str = "testing.txt"
    nombre_carpeta2: str = "testing2.txt"

    carpeta_falsa: Folder = Folder(
        id=id_test,
        nombre_original=nombre_carpeta,
        path=f"{config.UPLOAD_DIR}/{usuario.id}/{id_test}",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=usuario.id,
        usuario=usuario,
        id_carpeta=random_id
    )

    carpeta_falsa2: Folder = Folder(
        id=id_test2,
        nombre_original=nombre_carpeta2,
        path=f"{config.UPLOAD_DIR}/{usuario.id}/{id_test}",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=usuario.id,
        usuario=usuario,
        id_carpeta=random_id
    )

    carpetas_falsas = [carpeta_falsa, carpeta_falsa2]

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_dentro_carpeta") as mock_obtener:
        mock_obtener.return_value = carpetas_falsas

        response = client.get(f"/api/folders/{random_id}/folders")

    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response) == 2
    for i, carpeta in enumerate(carpetas_falsas):
        assert json_response[i]["id"] == str(carpeta.id)
        assert json_response[i]["nombre_original"] == carpeta.nombre_original
        assert json_response[i]["path"] == carpeta.path
        assert json_response[i]["id_usuario"] == str(carpeta.id_usuario)
        assert json_response[i]["nombre_usuario"] == usuario.nombre
        assert json_response[i]["id_carpeta"] == str(carpeta.id_carpeta)

    app.dependency_overrides.clear()
