from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.schemas.user_schemas import UserCreate, UserReturn
from app.schemas.auth_schemas import RegisterResponse
from app.services.user_service import crear_usuario

auth_router = APIRouter()


@auth_router.post("/register", response_model=RegisterResponse)
async def register(usuario: UserCreate, db: Session = Depends(get_db)):
    usuario_db: User = crear_usuario(usuario=usuario, db=db)

    return {
        "msg": "Usuario creado con exito",
        "usuario": UserReturn.model_validate(usuario_db)
    }
