import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.exceptions import IdYaUsadaException, NombreYaUsadoException
from app.models.folder import Folder
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user
from unittest.mock import patch

from app.config import config

client = TestClient(app=app)


def test_crear_carpeta_success():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_padre: uuid.UUID = uuid.uuid4()
    nombre_carpeta = "test.txt"

    id_hija: uuid.UUID = uuid.uuid4()

    carpeta_hija: Folder = Folder(
        id=id_hija,
        nombre_original=nombre_carpeta,
        path=f"{config.UPLOAD_DIR}/{usuario.id}/{id_padre}/{id_hija}",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=usuario.id,
        usuario=usuario,
        id_carpeta=id_padre
    )

    with patch("app.routes.folder_routes.folder_services.crear_carpeta_anidada") as mock_crear:
        mock_crear.return_value = carpeta_hija

        response = client.post(
            f"/api/folders/{id_padre}/folders", json={"nombre_carpeta": nombre_carpeta})

    resp_json = response.json()
    assert response.status_code == 200
    assert resp_json["msg"] == "Carpeta creada correctamente"
    assert resp_json["carpeta"]["id"] == str(id_hija)
    assert resp_json["carpeta"]["nombre_original"] == nombre_carpeta
    assert resp_json["carpeta"]["path"] == f"{config.UPLOAD_DIR}/{usuario.id}/{id_padre}/{id_hija}"
    assert resp_json["carpeta"]["fecha_creacion"] == "2026-01-21T01:44:31.825198"
    assert resp_json["carpeta"]["id_usuario"] == str(usuario.id)
    assert resp_json["carpeta"]["nombre_usuario"] == usuario.nombre
    assert resp_json["carpeta"]["id_carpeta"] == str(id_padre)

    app.dependency_overrides.clear()


def test_carpeta_id_usada():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test = uuid.uuid4()

    with patch("app.routes.folder_routes.folder_services.crear_carpeta_anidada") as mock_crear:
        mock_crear.side_effect = IdYaUsadaException(
            f"Ya se ha usado el ID {id_test}. Vuelve a subir la carpeta")

        response = client.post(
            f"/api/folders/{id_test}/folders", json={"nombre_carpeta": "test"})

    assert response.status_code == 409
    assert response.json()[
        "detail"] == f"Ya se ha usado el ID {id_test}. Vuelve a subir la carpeta"

    app.dependency_overrides.clear()


def test_carpeta_nombre_usado():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test = uuid.uuid4()
    nombre_carpeta = "test"

    with patch("app.routes.folder_routes.folder_services.crear_carpeta_anidada") as mock_crear:
        mock_crear.side_effect = NombreYaUsadoException(
            f"Ya has creado una carpeta con el nombre {nombre_carpeta}")

        response = client.post(
            f"/api/folders/{id_test}/folders", json={"nombre_carpeta": nombre_carpeta})

    assert response.status_code == 409
    assert response.json()[
        "detail"] == f"Ya has creado una carpeta con el nombre {nombre_carpeta}"

    app.dependency_overrides.clear()
