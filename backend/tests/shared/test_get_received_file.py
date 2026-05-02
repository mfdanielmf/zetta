import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.archivo_compartido import ArchivoCompartido
from app.models.user import User
from app.schemas import shared_file_schemas
from app.schemas.file_schemas import FileBase
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user
from unittest.mock import patch

client = TestClient(app=app)


def test_archivos_recibidos_success():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_compartido: uuid.UUID = uuid.uuid4()
    id_archivo: uuid.UUID = uuid.uuid4()

    archivo_falso: FileBase = FileBase(
        id=id_archivo,
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        nombre_usuario=usuario.nombre,
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

    with patch("app.routes.shared_routes.shared_file_services.obtener_archivos_compartidos_paginados") as mock_recibidos:
        mock_recibidos.return_value = (1, [archivo_compartido])

        response = client.get("/api/shared/received/files?page=1&limit=25")

    assert response.status_code == 200

    resp_json = response.json()

    assert resp_json["total"] == 1
    assert resp_json["pagina"] == 1
    assert resp_json["limite"] == 25
    assert len(resp_json["items"]) == 1

    item = resp_json["items"][0]

    assert item["propietario"]["id"] == str(usuario.id)
    assert item["propietario"]["correo"] == usuario.correo
    assert item["receptor"]["id"] == str(usuario_falso2.id)
    assert item["receptor"]["correo"] == usuario_falso2.correo

    assert item["archivo"]["id"] == str(archivo_falso.id)
    assert item["archivo"]["nombre_original"] == archivo_falso.nombre_original
    assert item["archivo"]["path"] == archivo_falso.path
    assert item["archivo"]["tamaño_bytes"] == archivo_falso.tamaño_bytes
    assert item["archivo"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_archivos_recibidos_vacio():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.shared_routes.shared_file_services.obtener_archivos_compartidos_paginados") as mock_recibidos:
        mock_recibidos.return_value = (0, [])

        response = client.get("/api/shared/received/files?page=1&limit=25")

    assert response.status_code == 200

    resp_json = response.json()

    assert resp_json["total"] == 0
    assert resp_json["items"] == []
    assert resp_json["pagina"] == 1
    assert resp_json["limite"] == 25

    app.dependency_overrides.clear()
