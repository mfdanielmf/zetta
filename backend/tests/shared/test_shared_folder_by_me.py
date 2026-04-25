import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.schemas import shared_folder_schemas
from app.schemas.folder_schemas import FolderBase
from app.schemas.shared_folder_schemas import CarpetaCompartidaBase
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user
from unittest.mock import patch

client = TestClient(app=app)


def test_carpetas_compartidos_por_mi_success():
    usuario = override_get_current_user()
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

    with patch("app.routes.shared_routes.shared_folder_services.obtener_carpetas_compartidas") as mock_compartidos:
        mock_compartidos.return_value = [carpeta_compartida]

        response = client.get("/api/shared/sent/folders")

    resp_json = response.json()
    assert response.status_code == 200

    assert len(resp_json) == 1
    assert resp_json[0]["propietario"]["id"] == str(usuario.id)
    assert resp_json[0]["propietario"]["correo"] == usuario.correo
    assert resp_json[0]["receptor"]["id"] == str(usuario_falso2.id)
    assert resp_json[0]["receptor"]["correo"] == usuario_falso2.correo
    assert resp_json[0]["carpeta"]["id"] == str(carpeta_falsa.id)
    assert resp_json[0]["carpeta"]["nombre_original"] == carpeta_falsa.nombre_original
    assert resp_json[0]["carpeta"]["path"] == carpeta_falsa.path
    assert resp_json[0]["carpeta"]["id_usuario"] == str(usuario.id)

    app.dependency_overrides.clear()


def test_carpetas_compartidas_por_mi_vacio():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.shared_routes.shared_folder_services.obtener_carpetas_compartidas") as mock_compartidos:
        mock_compartidos.return_value = []

        response = client.get("/api/shared/sent/folders")

    resp_json = response.json()
    assert response.status_code == 200

    assert len(resp_json) == 0

    app.dependency_overrides.clear()
