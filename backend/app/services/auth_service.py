
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from jose import jwt

from app.config import config

from app.models.user import User
from app.services.user_service import comprobar_hash_contraseña, obtener_usuario_nombre
from app.schemas.auth_schemas import LoginRequest, TokenData
from app.models.exceptions import ContraseñaIncorrectaException


def login_usuario(usuario_req: LoginRequest, db: Session) -> str:
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

    return token


def generar_access_token(data: TokenData):
    to_encode = data.model_dump()
    to_encode["id"] = str(to_encode["id"])

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)

    return encoded_jwt
