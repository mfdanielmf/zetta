from unittest.mock import patch
import uuid
from pathlib import Path
import os

from fastapi.testclient import TestClient

from app.models.exceptions import ArchivoNoEncontradoException
from app.models.file import File
from app.services.auth_services import get_current_user
from tests.util import override_get_current_user
from app.main import app

client = TestClient(app=app)


def test_descargar_archivo_id_formato_incorrecto():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    response = client.get("/api/files/idmuyreal")

    assert response.status_code == 422

    app.dependency_overrides.clear()


def test_descargar_archivo_id_inexistente():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    with patch("app.routes.file_routes.obtener_archivo_id") as mock_obtener:
        mock_obtener.side_effect = ArchivoNoEncontradoException()

        id_random: uuid.UUID = uuid.uuid4()

        response = client.get(f"/api/files/{id_random}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"No se ha encontrado el archivo con id {id_random}"
    }

    app.dependency_overrides.clear()


# Integración
def test_descargar_archivo_existente():
    usuario = override_get_current_user()
    app.dependency_overrides[get_current_user] = lambda: usuario

    RUTA = Path("uploads")
    RUTA.mkdir(exist_ok=True)
    os.makedirs("uploads", exist_ok=True)

    # Crear el archivo falso porque uso FileResponse que devuelve el archivo existente (después del test se borra)
    with open("uploads/testing.txt", "w") as f:
        f.write("Testingggg")

    archivo_falso = File(
        id=uuid.uuid4(),
        nombre_original="testing.txt",
        path="uploads/testing.txt",
        tamaño_bytes=10,
        fecha_creacion="2026-02-15T10:00:00",
        id_usuario=usuario.id,
        usuario=usuario
    )

    with patch("app.routes.file_routes.obtener_archivo_id") as mock_obtener:
        mock_obtener.return_value = archivo_falso

        id_random: uuid.UUID = uuid.uuid4()

        response = client.get(f"/api/files/{id_random}")

    assert response.status_code == 200

    app.dependency_overrides.clear()
    os.remove("uploads/testing.txt")
