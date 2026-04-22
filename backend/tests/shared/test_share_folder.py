import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.archivo_compartido import ArchivoCompartido
from app.models.carpeta_compartida import CarpetaCompartida
from app.models.exceptions import CarpetaNoEncontradaException, PropietarioException, YaCompartidoException, ArchivoNoEncontradoException, UsuarioNoEncontradoException
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user
from unittest.mock import patch

client = TestClient(app=app)


def test_crear_compartir_carpeta_success():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_compartido = uuid.uuid4()
    id_carpeta = uuid.uuid4()

    carpeta_falsa: Folder = Folder(
        id=id_carpeta,
        nombre_original="test",
        path=f"uploads/{usuario.id}/{id_carpeta}",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=usuario.id,
        usuario=usuario,
    )

    usuario_falso2 = User(
        id=uuid.uuid4(),
        nombre="test2",
        correo="test2@test.com",
        contraseña="test",
        fecha_creacion="2026-01-21T01:44:31.825198"
    )

    carpeta_compartida = CarpetaCompartida(
        id=id_compartido,
        fecha_compartido="2026-02-15T10:00:00",
        propietario=usuario,
        receptor=usuario_falso2,
        carpeta=carpeta_falsa
    )

    with patch("app.routes.shared_routes.shared_folder_services.compartir_carpeta") as mock_compartir:
        mock_compartir.return_value = carpeta_compartida

        response = client.post(
            "/api/shared/folders", json={"id_carpeta": str(carpeta_falsa.id), "correo_usuario": usuario_falso2.correo}
        )

    resp_json = response.json()["carpeta_compartida"]

    assert response.status_code == 200
    assert resp_json["propietario"]["id"] == str(usuario.id)
    assert resp_json["propietario"]["correo"] == usuario.correo
    assert resp_json["receptor"]["id"] == str(usuario_falso2.id)
    assert resp_json["receptor"]["correo"] == usuario_falso2.correo
    assert resp_json["carpeta"]["id"] == str(carpeta_falsa.id)
    assert resp_json["carpeta"]["nombre_original"] == carpeta_falsa.nombre_original
    assert resp_json["carpeta"]["path"] == carpeta_falsa.path
    assert resp_json["carpeta"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_compartir_carpeta_usuario_es_propietario():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_folder_services.compartir_carpeta") as mock_compartir:
        mock_compartir.side_effect = PropietarioException(
            "Ya eres el propietario")

        response = client.post(
            "/api/shared/folders", json={"id_carpeta": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Ya eres el propietario"

    app.dependency_overrides.clear()


def test_carpeta_ya_compartida():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_folder_services.compartir_carpeta") as mock_compartir:
        mock_compartir.side_effect = YaCompartidoException("Ya compartido")

        response = client.post(
            "/api/shared/folders", json={"id_carpeta": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 409
    assert response.json()["detail"] == "Ya compartido"

    app.dependency_overrides.clear()


def test_compartir_carpeta_no_encontrada():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_folder_services.compartir_carpeta") as mock_compartir:
        mock_compartir.side_effect = CarpetaNoEncontradaException(
            "No encontrada")

        response = client.post(
            "/api/shared/folders", json={"id_carpeta": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "No encontrada"

    app.dependency_overrides.clear()


def test_compartir_carpeta_receptor_no_encontrado():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_folder_services.compartir_carpeta") as mock_compartir:
        mock_compartir.side_effect = UsuarioNoEncontradoException(
            "Usuario no encontrado")

        response = client.post(
            "/api/shared/folders", json={"id_carpeta": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

    app.dependency_overrides.clear()
