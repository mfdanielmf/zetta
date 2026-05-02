
from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.config import config

from app.models.user import User
from app.services.user_services import comprobar_hash_contraseña, obtener_usuario_nombre
from app.schemas.auth_schemas import LoginRequest, TokenData
from app.models.exceptions import UsuarioNoEncontradoException, ContraseñaIncorrectaException, UsuarioNoAutenticadoException


def login_usuario(usuario_req: LoginRequest, db: Session) -> tuple[str, User]:
    """
    UsuarioNoEncontradoException, ContraseñaIncorrectaException
    """
    usuario: User = obtener_usuario_nombre(nombre=usuario_req.nombre, db=db)

    contraseña_correcta: bool = comprobar_hash_contraseña(
        usuario=usuario, contraseña=usuario_req.contraseña)

    if contraseña_correcta is False:
        raise ContraseñaIncorrectaException("La contraseña es incorrecta")

    token_data = TokenData(
        id=usuario.id, nombre=usuario.nombre, correo=usuario.correo)

    token: str = generar_access_token(token_data)

    return token, usuario


def generar_access_token(data: TokenData):
    to_encode = data.model_dump()
    to_encode["id"] = str(to_encode["id"])

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)

    return encoded_jwt


def obtener_usuario_jwt(token: str, db: Session) -> User:
    """
    UsuarioNoEncontradoException, UsuarioNoAutenticadoException
    """
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY,
                             algorithms=[config.ALGORITHM])
        id: uuid.UUID = payload.get("id")
        nombre_usuario: str = payload.get("nombre")
        correo: str = payload.get("correo")

        if nombre_usuario is None:
            raise UsuarioNoEncontradoException()

        token_data = TokenData(id=id, nombre=nombre_usuario, correo=correo)
    except JWTError:
        raise UsuarioNoAutenticadoException()

    user: User = obtener_usuario_nombre(nombre=token_data.nombre, db=db)

    return user
