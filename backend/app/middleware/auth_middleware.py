# Middleware para inyectar en las rutas
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.exceptions import UsuarioNoAutenticadoException, UsuarioNoEncontradoException
from app.models.user import User
from app.services.auth_services import obtener_usuario_jwt


class BearerCustom(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=False)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="No se proporcionó token"
            )

        return credentials


security = BearerCustom()


def get_current_user(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    HTTPException
    """
    access_token = credentials.credentials

    try:
        return obtener_usuario_jwt(access_token, db)
    except UsuarioNoEncontradoException:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except UsuarioNoAutenticadoException:
        raise HTTPException(
            status_code=401, detail="Token incorrecto o expirado")
