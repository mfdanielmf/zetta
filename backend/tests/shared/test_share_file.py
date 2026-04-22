import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.archivo_compartido import ArchivoCompartido
from app.models.exceptions import PropietarioException, YaCompartidoException, ArchivoNoEncontradoException, UsuarioNoEncontradoException
from app.models.file import File
from app.models.user import User
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user
from unittest.mock import patch

client = TestClient(app=app)


def test_crear_compartir_archivo_success():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_compartido: uuid.UUID = uuid.uuid4()
    id_archivo: uuid.UUID = uuid.uuid4()

    archivo_falso: File = File(
        id=id_archivo,
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario
    )

    usuario_falso2: User = User(
        id=uuid.uuid4(),
        nombre="test2",
        correo="test2@test.com",
        contraseña="test",
        fecha_creacion="2026-01-21T01:44:31.825198"
    )

    archivo_compartido: ArchivoCompartido = ArchivoCompartido(
        id=id_compartido,
        fecha_compartido="2026-02-15T10:00:00",
        propietario=usuario,
        receptor=usuario_falso2,
        archivo=archivo_falso
    )

    with patch("app.routes.shared_routes.shared_file_services.compartir_archivo") as mock_compartir:
        mock_compartir.return_value = archivo_compartido

        response = client.post(
            "/api/shared/files", json={"id_archivo": str(archivo_falso.id), "correo_usuario": usuario_falso2.correo})

    resp_json = response.json()["archivo_compartido"]
    assert response.status_code == 200
    assert resp_json["propietario"]["id"] == str(usuario.id)
    assert resp_json["propietario"]["correo"] == usuario.correo
    assert resp_json["receptor"]["id"] == str(usuario_falso2.id)
    assert resp_json["receptor"]["correo"] == usuario_falso2.correo
    assert resp_json["archivo"]["id"] == str(archivo_falso.id)
    assert resp_json["archivo"]["nombre_original"] == archivo_falso.nombre_original
    assert resp_json["archivo"]["path"] == archivo_falso.path
    assert resp_json["archivo"]["tamaño_bytes"] == archivo_falso.tamaño_bytes
    assert resp_json["archivo"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_compartir_archivo_usuario_es_propietario():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_file_services.compartir_archivo") as mock_compartir:
        mock_compartir.side_effect = PropietarioException(
            "Ya eres el propietario")

        response = client.post(
            "/api/shared/files", json={"id_archivo": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Ya eres el propietario"

    app.dependency_overrides.clear()


def test_archivo_ya_compartido():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_file_services.compartir_archivo") as mock_compartir:
        mock_compartir.side_effect = YaCompartidoException("Ya compartido")

        response = client.post(
            "/api/shared/files", json={"id_archivo": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 409
    assert response.json()["detail"] == "Ya compartido"

    app.dependency_overrides.clear()


def test_compartir_archivo_no_encontrado():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_file_services.compartir_archivo") as mock_compartir:
        mock_compartir.side_effect = ArchivoNoEncontradoException(
            "No encontrado")

        response = client.post(
            "/api/shared/files", json={"id_archivo": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "No encontrado"

    app.dependency_overrides.clear()


def test_compartir_receptor_no_encontrado():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_test: uuid.UUID = uuid.uuid4()

    with patch("app.routes.shared_routes.shared_file_services.compartir_archivo") as mock_compartir:
        mock_compartir.side_effect = UsuarioNoEncontradoException(
            "Usuario no encontrado")

        response = client.post(
            "/api/shared/files", json={"id_archivo": str(id_test), "correo_usuario": usuario.correo}
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

    app.dependency_overrides.clear()
