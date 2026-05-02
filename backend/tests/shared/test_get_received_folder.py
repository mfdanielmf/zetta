import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas import shared_folder_schemas
from app.schemas.folder_schemas import FolderBase
from app.schemas.shared_folder_schemas import CarpetaCompartidaBase
from tests.util import override_get_current_user
from unittest.mock import patch

client = TestClient(app=app)


def test_carpetas_compartidos_por_mi_success():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_compartido: uuid.UUID = uuid.uuid4()
    id_carpeta: uuid.UUID = uuid.uuid4()

    carpeta_falsa: FolderBase = FolderBase(
        id=id_carpeta,
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario,
        nombre_usuario=usuario.nombre,
    )

    usuario_falso2: User = User(
        id=uuid.uuid4(),
        nombre="test2",
        correo="test2@test.com",
        contraseña="test",
        fecha_creacion="2026-01-21T01:44:31.825198"
    )

    carpeta_compartida: CarpetaCompartidaBase = shared_folder_schemas.CarpetaCompartidaBase(
        id=id_compartido,
        fecha_compartido="2026-02-15T10:00:00",
        propietario=usuario,
        receptor=usuario_falso2,
        carpeta=carpeta_falsa
    )

    with patch("app.routes.shared_routes.shared_folder_services.obtener_carpetas_recibidas_paginadas") as mock_compartidos:
        mock_compartidos.return_value = (1, [carpeta_compartida])

        response = client.get("/api/shared/received/folders?page=1&limit=25")

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

    assert item["carpeta"]["id"] == str(carpeta_falsa.id)
    assert item["carpeta"]["nombre_original"] == carpeta_falsa.nombre_original
    assert item["carpeta"]["path"] == carpeta_falsa.path
    assert item["carpeta"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_carpetas_compartidas_por_mi_vacio():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.shared_routes.shared_folder_services.obtener_carpetas_recibidas_paginadas") as mock_compartidos:
        mock_compartidos.return_value = (0, [])

        response = client.get("/api/shared/received/folders?page=1&limit=25")

    assert response.status_code == 200

    resp_json = response.json()

    assert resp_json["total"] == 0
    assert resp_json["items"] == []
    assert resp_json["pagina"] == 1
    assert resp_json["limite"] == 25

    app.dependency_overrides.clear()
