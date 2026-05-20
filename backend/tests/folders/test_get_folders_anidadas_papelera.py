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


def test_get_anidadas_carpeta_que_no_esta_en_papelera():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_carpeta_papelera_paginadas") as mock_obtener:
        mock_obtener.side_effect = CarpetaNoEncontradaException()

        response = client.get(
            f"/api/folders/trash/{id_carpeta}/folders?page=1&limit=25")

    assert response.status_code == 404
    assert response.json()[
        "detail"] == f"No se ha encontrado la carpeta con id {id_carpeta} en la papelera"

    app.dependency_overrides.clear()


def test_get_anidadas_papelera_sin_carpetas():
    app.dependency_overrides[get_current_user] = override_get_current_user

    random_id: uuid.UUID = uuid.uuid4()

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_carpeta_papelera_paginadas") as mock_obtener:
        mock_obtener.return_value = (0, [])

        response = client.get(
            f"/api/folders/trash/{random_id}/folders?page=1&limit=25")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["items"] == []
    assert json_response["total"] == 0

    app.dependency_overrides.clear()


def test_get_anidadas_papelera_con_una_carpeta():
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
        fecha_eliminacion="2026-01-21T01:44:31.825198",
        id_carpeta=random_id,
        favorito=False
    )

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_carpeta_papelera_paginadas") as mock_obtener:
        mock_obtener.return_value = (1, [carpeta_falsa])

        response = client.get(
            f"/api/folders/trash/{random_id}/folders?page=1&limit=25")

    json_response = response.json()

    assert response.status_code == 200
    assert json_response["total"] == 1
    assert len(json_response["items"]) == 1

    item = json_response["items"][0]

    assert item["id"] == str(carpeta_falsa.id)
    assert item["nombre_original"] == nombre_carpeta
    assert item["nombre_usuario"] == usuario.nombre
    assert item["id_carpeta"] == str(random_id)
    assert item["fecha_eliminacion"] == carpeta_falsa.fecha_eliminacion

    app.dependency_overrides.clear()


def test_get_anidadas_con_varias_carpetas_papelera():
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
        fecha_eliminacion="2026-01-21T01:44:31.825198",
        id_carpeta=random_id,
        favorito=False
    )

    carpeta_falsa2: Folder = Folder(
        id=id_test2,
        nombre_original=nombre_carpeta2,
        path=f"{config.UPLOAD_DIR}/{usuario.id}/{id_test}",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=usuario.id,
        usuario=usuario,
        fecha_eliminacion="2026-01-21T01:44:31.825198",
        id_carpeta=random_id,
        favorito=False
    )

    carpetas_falsas = [carpeta_falsa, carpeta_falsa2]

    with patch("app.routes.folder_routes.folder_services.obtener_carpetas_carpeta_papelera_paginadas") as mock_obtener:
        mock_obtener.return_value = (2, carpetas_falsas)

        response = client.get(
            f"/api/folders/trash/{random_id}/folders?page=1&limit=25")

    json_response = response.json()

    assert response.status_code == 200
    assert json_response["total"] == 2
    assert len(json_response["items"]) == 2

    for i, carpeta in enumerate(carpetas_falsas):
        item = json_response["items"][i]

        assert item["id"] == str(carpeta.id)
        assert item["nombre_original"] == carpeta.nombre_original
        assert item["path"] == carpeta.path
        assert item["id_usuario"] == str(carpeta.id_usuario)
        assert item["nombre_usuario"] == usuario.nombre
        assert item["id_carpeta"] == str(carpeta.id_carpeta)
        assert item["fecha_eliminacion"] == carpeta.fecha_eliminacion

    app.dependency_overrides.clear()
