import io
import uuid
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, patch
from app.models.exceptions import NombreYaUsadoException, IdYaUsadaException, TamañoExcedidoException
from app.models.file import File
from app.models.user import User
from app.schemas.file_schemas import FileResponse
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user

client = TestClient(app)


def test_subir_archivo():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id: uuid.UUID = uuid.uuid4()
    usuario_falso: User = User(id=id, nombre="testinggg")
    archivo_falso: File = File(
        id=id,
        nombre_original="test.txt",
        tamaño_bytes="20",
        path=f"uploads/{id}.txt",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=id,
        usuario=usuario_falso,
        favorito=False
    )

    with patch("app.routes.file_routes.file_services.guardar_archivo", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.return_value = archivo_falso

        response = client.post("/api/files", files={
            "file_upload": ("test.txt", io.BytesIO(b"Test"), "text/plain")
        })

    archivo_response: FileResponse = FileResponse.model_validate(
        response.json())

    assert response.status_code == 200
    assert archivo_response.archivos[0].id == archivo_falso.id
    assert archivo_response.archivos[0].nombre_original == archivo_falso.nombre_original
    assert archivo_response.archivos[0].path == archivo_falso.path
    assert archivo_response.archivos[0].id_usuario == archivo_falso.id_usuario
    assert archivo_response.archivos[0].nombre_usuario == usuario_falso.nombre

    app.dependency_overrides.clear()


def test_subir_sin_archivo():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.post("/api/files")

    assert response.status_code == 422

    app.dependency_overrides.clear()


def test_subir_varios_archivos():
    app.dependency_overrides[get_current_user] = override_get_current_user

    id: uuid.UUID = uuid.uuid4()
    usuario_falso: User = User(id=id, nombre="testinggg")
    archivo_falso: File = File(
        id=id,
        nombre_original="test.txt",
        tamaño_bytes="20",
        path=f"uploads/{id}.txt",
        fecha_creacion="2026-01-21T01:44:31.825198",
        id_usuario=id,
        usuario=usuario_falso,
        favorito=False
    )

    archivo_falso2: File = File(
        id=id,
        nombre_original="test2.txt",
        tamaño_bytes="100",
        path=f"uploads/{id}.txt",
        fecha_creacion="2026-01-22T01:44:31.825198",
        id_usuario=id,
        usuario=usuario_falso,
        favorito=False
    )

    archivos_falsos = [archivo_falso, archivo_falso2]

    with patch("app.routes.file_routes.file_services.guardar_archivo", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.side_effect = archivos_falsos

        response = client.post("/api/files", files=[
            ("file_upload", ("test1.txt", io.BytesIO(b"Test1"), "text/plain")),
            ("file_upload", ("test2.txt", io.BytesIO(b"Test2"), "text/plain"))
        ])

    archivo_response: FileResponse = FileResponse.model_validate(
        response.json())

    assert response.status_code == 200
    for i, archivo in enumerate(archivos_falsos):
        assert archivo_response.archivos[i].id == archivo.id
        assert archivo_response.archivos[i].nombre_original == archivo.nombre_original
        assert archivo_response.archivos[i].path == archivo.path
        assert archivo_response.archivos[i].id_usuario == archivo.id_usuario
        assert archivo_response.archivos[i].nombre_usuario == usuario_falso.nombre

    app.dependency_overrides.clear()


def test_subir_archivo_nombre_usado():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.file_routes.file_services.guardar_archivo", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.side_effect = NombreYaUsadoException(
            "Ya hay un archivo con ese nombre")

        response = client.post(
            "/api/files", files=[("file_upload", ("test.txt", io.BytesIO(b"Test"), "text/plain"))]
        )

    assert response.status_code == 409
    assert response.json()["detail"] == "Ya hay un archivo con ese nombre"

    app.dependency_overrides.clear()


def test_subir_archivo_id_usada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.file_routes.file_services.guardar_archivo", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.side_effect = IdYaUsadaException(
            "Ya se ha usado la ID. Vuelve a subir el archivo")

        response = client.post(
            "/api/files", files=[("file_upload", ("test.txt", io.BytesIO(b"Test"), "text/plain"))]
        )

    assert response.status_code == 409
    assert response.json()[
        "detail"] == "Ya se ha usado la ID. Vuelve a subir el archivo"

    app.dependency_overrides.clear()


def test_subir_archivo_id_usada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.file_routes.file_services.guardar_archivo", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.side_effect = IdYaUsadaException(
            "Ya se ha usado la ID. Vuelve a subir el archivo")

        response = client.post(
            "/api/files", files=[("file_upload", ("test.txt", io.BytesIO(b"Test"), "text/plain"))]
        )

    assert response.status_code == 409
    assert response.json()[
        "detail"] == "Ya se ha usado la ID. Vuelve a subir el archivo"

    app.dependency_overrides.clear()


def test_subir_archivo_tamaño_excedido():
    app.dependency_overrides[get_current_user] = override_get_current_user

    with patch("app.routes.file_routes.file_services.guardar_archivo", new_callable=AsyncMock) as mock_guardar:
        mock_guardar.side_effect = TamañoExcedidoException(
            f"Has excedido el tamaño máximo de subida")

        response = client.post(
            "/api/files", files=[("file_upload", ("test.txt", io.BytesIO(b"Test"), "text/plain"))]
        )

    assert response.status_code == 413
    assert response.json()[
        "detail"] == "Has excedido el tamaño máximo de subida"

    app.dependency_overrides.clear()
