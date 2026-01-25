import io
import uuid
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, patch
from app.models.file import File
from app.models.user import User
from app.schemas.file_schemas import FileResponse
from app.services.auth_services import get_current_user

client = TestClient(app)


def override_get_current_user() -> User:
    return User(id=uuid.uuid4(), nombre="test", correo="test@test.com", contraseña="test", fecha_creacion="2026-01-21T01:44:31.825198")


app.dependency_overrides[get_current_user] = override_get_current_user


def test_subir_archivo():
    id: uuid.UUID = uuid.uuid4()
    archivo_falso: File = File(id=id, nombre_original="test.txt",
                               path=f"uploads/{id}.txt", fecha_creacion="2026-01-21T01:44:31.825198", id_usuario=id)

    with patch("app.routes.file_routes.guardar_archivo", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.return_value = archivo_falso

        response = client.post("/api/files", files={
            "file_upload": ("test.txt", io.BytesIO(b"Test"), "text/plain")
        })

    archivo_response: FileResponse = FileResponse.model_validate(
        response.json())

    assert response.status_code == 200
    assert archivo_response.archivo.id == archivo_falso.id
    assert archivo_response.archivo.nombre_original == archivo_falso.nombre_original
    assert archivo_response.archivo.path == archivo_falso.path
    assert archivo_response.archivo.id_usuario == archivo_falso.id_usuario
