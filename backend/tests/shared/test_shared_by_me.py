import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.archivo_compartido import ArchivoCompartido
from app.models.exceptions import PropietarioException, YaCompartidoException, ArchivoNoEncontradoException, UsuarioNoEncontradoException
from app.models.file import File
from app.models.user import User
from app.schemas import shared_file_schemas
from app.schemas.file_schemas import FileBase
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user
from unittest.mock import patch

client = TestClient(app=app)


def test_archivos_compartidos_por_mi_success():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_compartido: uuid.UUID = uuid.uuid4()
    id_archivo: uuid.UUID = uuid.uuid4()

    archivo_falso: File = FileBase(
        id=id_archivo,
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario,
        nombre_usuario=usuario.nombre,
        id_carpeta=None
    )

    usuario_falso2: User = User(
        id=uuid.uuid4(),
        nombre="test2",
        correo="test2@test.com",
        contraseña="test",
        fecha_creacion="2026-01-21T01:44:31.825198"
    )

    archivo_compartido: ArchivoCompartido = shared_file_schemas.ArchivoCompartidoBase(
        id=id_compartido,
        fecha_compartido="2026-02-15T10:00:00",
        propietario=usuario,
        receptor=usuario_falso2,
        archivo=archivo_falso
    )

    with patch("app.routes.shared_routes.shared_file_services.obtener_archivos_compartidos") as mock_compartidos:
        mock_compartidos.return_value = [archivo_compartido]

        response = client.get("/api/shared/files")

    resp_json = response.json()
    assert response.status_code == 200

    assert len(resp_json) == 1
    assert resp_json[0]["propietario"]["id"] == str(usuario.id)
    assert resp_json[0]["propietario"]["correo"] == usuario.correo
    assert resp_json[0]["receptor"]["id"] == str(usuario_falso2.id)
    assert resp_json[0]["receptor"]["correo"] == usuario_falso2.correo
    assert resp_json[0]["archivo"]["id"] == str(archivo_falso.id)
    assert resp_json[0]["archivo"]["nombre_original"] == archivo_falso.nombre_original
    assert resp_json[0]["archivo"]["path"] == archivo_falso.path
    assert resp_json[0]["archivo"]["tamaño_bytes"] == archivo_falso.tamaño_bytes
    assert resp_json[0]["archivo"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_archivos_compartidos_por_mi_vacio():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.shared_routes.shared_file_services.obtener_archivos_compartidos") as mock_compartidos:
        mock_compartidos.return_value = []

        response = client.get("/api/shared/files")

    resp_json = response.json()
    assert response.status_code == 200

    assert len(resp_json) == 0

    app.dependency_overrides.clear()
