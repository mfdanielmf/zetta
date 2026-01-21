from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app.models.exceptions import CorreoYaUsadoException, NombreYaUsadoException
from app.schemas.user_schemas import UserCreate
from app.repositories.user_repo import insert_user_db, get_user_by_email, get_user_by_name
from sqlalchemy.orm import Session


def crear_usuario(usuario: UserCreate, db: Session) -> User:
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
