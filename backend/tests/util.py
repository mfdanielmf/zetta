import uuid

from app.models.user import User


def override_get_current_user() -> User:
    return User(id=uuid.uuid4(), nombre="test", correo="test@test.com", contraseña="test", fecha_creacion="2026-01-21T01:44:31.825198")
