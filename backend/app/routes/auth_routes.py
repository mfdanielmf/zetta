from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.models.exceptions import CorreoYaUsadoException, NombreYaUsadoException, UsuarioNoEncontradoException, ContraseñaIncorrectaException
from app.schemas.user_schemas import UserCreate, UserReturn
from app.schemas.auth_schemas import RegisterResponse, LoginRequest
from app.services.user_service import crear_usuario
from app.services.auth_service import login_usuario

auth_router = APIRouter()


@auth_router.post("/register", response_model=RegisterResponse)
def register(usuario: UserCreate, db: Session = Depends(get_db)):
    try:
        usuario_db: User = crear_usuario(usuario=usuario, db=db)

        return {
            "msg": "Usuario creado con exito",
            "usuario": UserReturn.model_validate(usuario_db)
        }
    except CorreoYaUsadoException as e1:
        raise HTTPException(status_code=400, detail=str(e1))
    except NombreYaUsadoException as e2:
        raise HTTPException(status_code=400, detail=str(e2))


@auth_router.post("/login")
def login(usuario_req: LoginRequest, db: Session = Depends(get_db)):
    try:
        token: str = login_usuario(usuario_req=usuario_req, db=db)

        return token
    except UsuarioNoEncontradoException as e1:
        raise HTTPException(status_code=404, detail=str(e1))
    except ContraseñaIncorrectaException as e2:
        raise HTTPException(status_code=400, detail=str(e2))
