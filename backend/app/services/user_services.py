from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.models.exceptions import (
    CorreoYaUsadoException,
    NombreYaUsadoException,
    UsuarioNoEncontradoException,
)
from app.models.user import User
from app.repositories.user_repo import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_name,
    insert_user_db,
)
from app.schemas.user_schemas import UserCreate


_hasher = PasswordHasher()


def generar_hash_contraseña(contraseña: str) -> str:
    return _hasher.hash(contraseña)


def comprobar_hash_contraseña(usuario: User, contraseña: str) -> bool:
    try:
        _hasher.verify(hash=usuario.contraseña, password=contraseña)
    except VerifyMismatchError:
        return False

    return True


def obtener_usuario_nombre(nombre: str, db: Session) -> User:
    """
    UsuarioNoEncontradoException
    """

    usuario: User | None = get_user_by_name(nombre=nombre, db=db)

    if usuario is None:
        raise UsuarioNoEncontradoException("Usuario no encontrado")

    return usuario


def crear_usuario(usuario: UserCreate, db: Session) -> User:
    """
    NombreYaUsadoException, CorreoYaUsadoException
    """

    if get_user_by_name(nombre=usuario.nombre, db=db) is not None:
        raise NombreYaUsadoException(
            f"Ya se ha encontrado un usuario con nombre {usuario.nombre}"
        )

    if get_user_by_email(correo=usuario.correo, db=db) is not None:
        raise CorreoYaUsadoException(
            f"Ya se ha encontrado un usuario con el correo {usuario.correo}"
        )

    hash_contraseña: str = generar_hash_contraseña(usuario.contraseña)

    usuario_model: User = User(
        nombre=usuario.nombre, correo=usuario.correo, contraseña=hash_contraseña
    )

    usuario_db: User = insert_user_db(usuario=usuario_model, db=db)

    return usuario_db


def obtener_usuario_id(id: str, db: Session) -> User:
    """
    UsuarioNoEncontradoException
    """
    usuario: User | None = get_user_by_id(id=id, db=db)

    if usuario is None:
        raise UsuarioNoEncontradoException("Usuario no encontrado")

    return usuario


def obtener_usuario_correo(correo: EmailStr, db: Session) -> User:
    """
    UsuarioNoEncontradoException
    """
    usuario: User | None = get_user_by_email(correo=correo, db=db)

    if usuario is None:
        raise UsuarioNoEncontradoException("Usuario no encontrado")

    return usuario
