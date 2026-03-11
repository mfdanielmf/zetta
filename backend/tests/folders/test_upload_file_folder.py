import io
import uuid

from fastapi.testclient import TestClient
from app.main import app
from app.models.file import File
from app.models.user import User
from app.services.auth_services import get_current_user
from app.schemas.folder_schemas import UploadFileFolderResponse
from tests.util import override_get_current_user
from unittest.mock import patch, AsyncMock

client = TestClient(app=app)


def test_subir_archivo_carpeta():
    usuario: User = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    id_carpeta: uuid.UUID = uuid.uuid4()
    id_archivo: uuid.UUID = uuid.uuid4()

    archivo_falso: File = File(
        id=id_archivo,
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        id_carpeta=id_carpeta,
        usuario=usuario
    )

    with patch("app.routes.folder_routes.guardar_archivo_carpeta", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.return_value = archivo_falso

        response = client.post(f"/api/folders/{id_carpeta}/files", files={
            "archivo": ("testing.txt", io.BytesIO(b"Test"), "text/plain")
        })

    json_response: UploadFileFolderResponse = UploadFileFolderResponse.model_validate(
        response.json())

    assert response.status_code == 200
    assert json_response.msg == "Archivo subido correctamente"
    assert json_response.archivo.id == id_archivo
    assert json_response.archivo.id_usuario == usuario.id
    assert json_response.archivo.nombre_original == "testing.txt"
    assert json_response.archivo.id_carpeta == id_carpeta

    app.dependency_overrides.clear()
