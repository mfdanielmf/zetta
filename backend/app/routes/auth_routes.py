from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.models.exceptions import CorreoYaUsadoException, NombreYaUsadoException, UsuarioNoEncontradoException, ContraseñaIncorrectaException, UsuarioNoAutenticadoException
from app.schemas.user_schemas import UserCreate, UserReturn
from app.schemas.auth_schemas import RegisterResponse, LoginRequest, LoginResponse, MeResponse, LogoutResponse
from app.services.user_services import crear_usuario
from app.services.auth_services import login_usuario, obtener_usuario_jwt
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

        response = JSONResponse(content={
            "msg": "Sesión iniciada correctamente",
            "usuario": UserReturn.model_validate(usuario).model_dump(mode="json")
        })

        response.set_cookie(key="access_token", value=token, samesite="lax",
                            httponly=True, max_age=3600, expires=3600)

        return response
    except UsuarioNoEncontradoException as e1:
        raise HTTPException(status_code=404, detail=str(e1))
    except ContraseñaIncorrectaException as e2:
        raise HTTPException(status_code=400, detail=str(e2))


@auth_router.get("/me", response_model=MeResponse)
def me(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    try:
        usuario: User = obtener_usuario_jwt(token=token, db=db)

        return {
            "usuario": UserReturn.model_validate(usuario)
        }
    except UsuarioNoEncontradoException:
        raise HTTPException(
            status_code=404, detail="No se ha encontrado el usuario")
    except UsuarioNoAutenticadoException:
        raise HTTPException(status_code=400, detail="Token incorrecto")


@auth_router.post("/logout", response_model=LogoutResponse)
@limiter.limit(AUTH_RATE_LIMIT)
def logout(request: Request):
    response = JSONResponse(content={
        "msg": "Sesión cerrada con éxito"
    })
    response.delete_cookie("access_token")

    return response
