from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.models.exceptions import CorreoYaUsadoException, NombreYaUsadoException, UsuarioNoEncontradoException, ContraseñaIncorrectaException
from app.schemas.user_schemas import UserCreate, UserReturn
from app.schemas.auth_schemas import RegisterResponse, LoginRequest, LoginResponse, MeResponse
from app.services.user_services import crear_usuario
from app.services.auth_services import login_usuario
from app.core.limiter import limiter, AUTH_RATE_LIMIT


auth_router = APIRouter()


@auth_router.post("/register", response_model=RegisterResponse)
@limiter.limit(AUTH_RATE_LIMIT)
def register(request: Request, usuario: UserCreate, db: Session = Depends(get_db)):
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


@auth_router.post("/login", response_model=LoginResponse)
@limiter.limit(AUTH_RATE_LIMIT)
def login(request: Request, usuario_req: LoginRequest, db: Session = Depends(get_db)):
    try:
        token, usuario = login_usuario(usuario_req=usuario_req, db=db)

        return {
            "msg": "Sesión iniciada correctamente",
            "usuario": UserReturn.model_validate(usuario).model_dump(mode="json"),
            "token": token
        }
    except UsuarioNoEncontradoException as e1:
        raise HTTPException(status_code=404, detail=str(e1))
    except ContraseñaIncorrectaException as e2:
        raise HTTPException(status_code=400, detail=str(e2))


@auth_router.get("/me", response_model=MeResponse)
def me(usuario: User = Depends(get_current_user)):
    return {
        "usuario": UserReturn.model_validate(usuario)
    }
