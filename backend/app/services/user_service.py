from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app.models.exceptions import CorreoYaUsadoException, NombreYaUsadoException, UsuarioNoEncontradoException
from app.schemas.auth_schemas import LoginRequest
from app.schemas.user_schemas import UserCreate
from app.repositories.user_repo import insert_user_db, get_user_by_email, get_user_by_name
from sqlalchemy.orm import Session


def obtener_usuario_nombre(nombre: str, db: Session) -> User:
    """
    UsuarioNoEncontradoException
    """

    usuario: User | None = get_user_by_name(nombre=nombre, db=db)

    if usuario is None:
        raise UsuarioNoEncontradoException(
            f"No se ha encontrado el usuario con nombre {nombre}")

    return usuario


def crear_usuario(usuario: UserCreate, db: Session) -> User:
    """
    NombreYaUsadoException, CorreoYaUsadoException
    """

    if get_user_by_name(nombre=usuario.nombre, db=db) is not None:
        raise NombreYaUsadoException(
            f"Ya se ha encontrado un usuario con nombre {usuario.nombre}")

    if get_user_by_email(correo=usuario.correo, db=db) is not None:
        raise CorreoYaUsadoException(
            f"Ya se ha encontrado un usuario con el correo {usuario.correo}")

    hash: str = generate_password_hash(password=usuario.contraseña)

    usuario_model: User = User(nombre=usuario.nombre,
                               correo=usuario.correo, contraseña=hash)

    usuario_db: User = insert_user_db(usuario=usuario_model, db=db)

    return usuario_db


def comprobar_hash_contraseña(usuario: User, contraseña: str) -> bool:
    return check_password_hash(pwhash=usuario.contraseña, password=contraseña)
