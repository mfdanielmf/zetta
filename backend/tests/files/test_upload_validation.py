import io
import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.middleware.auth_middleware import get_current_user
from tests.util import override_get_current_user

client = TestClient(app)


def test_subir_archivo_extension_exe_rechazada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.post(
        "/api/files",
        files={
            "file_upload": (
                "malware.exe",
                io.BytesIO(b"MZ"),
                "application/x-msdownload",
            )
        },
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "Extensión '.exe' no permitida"

    app.dependency_overrides.clear()


def test_subir_archivo_extension_sh_rechazada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.post(
        "/api/files",
        files={"file_upload": ("script.sh", io.BytesIO(b"#!/bin/sh"), "text/x-sh")},
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "Extensión '.sh' no permitida"

    app.dependency_overrides.clear()


def test_subir_archivo_sin_extension_rechazada():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.post(
        "/api/files",
        files={
            "file_upload": ("sin_extension", io.BytesIO(b"contenido"), "text/plain")
        },
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "El archivo no tiene extensión"

    app.dependency_overrides.clear()


def test_subir_archivo_carpeta_extension_exe_rechazada():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    response = client.post(
        f"/api/folders/{id_carpeta}/files",
        files={
            "file_upload": (
                "malware.exe",
                io.BytesIO(b"MZ"),
                "application/x-msdownload",
            )
        },
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "Extensión '.exe' no permitida"

    app.dependency_overrides.clear()


def test_subir_archivo_carpeta_sin_extension_rechazada():
    app.dependency_overrides[get_current_user] = override_get_current_user
    id_carpeta: uuid.UUID = uuid.uuid4()

    response = client.post(
        f"/api/folders/{id_carpeta}/files",
        files={
            "file_upload": ("sin_extension", io.BytesIO(b"contenido"), "text/plain")
        },
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "El archivo no tiene extensión"

    app.dependency_overrides.clear()
