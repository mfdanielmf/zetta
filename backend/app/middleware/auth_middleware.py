# Middleware para inyectar en las rutas
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.exceptions import UsuarioNoAutenticadoException, UsuarioNoEncontradoException
from app.models.user import User
from app.services.auth_services import obtener_usuario_jwt


def get_current_user(db: Session = Depends(get_db), access_token: str = Cookie(None)) -> User:
    """
    HTTPException
    """
    if access_token is None:
        raise HTTPException(
            401,
            detail="No se proporcionó token"
        )

    try:
        return obtener_usuario_jwt(access_token, db)
    except UsuarioNoEncontradoException:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except UsuarioNoAutenticadoException:
        raise HTTPException(
            status_code=401, detail="Token incorrecto o expirado")