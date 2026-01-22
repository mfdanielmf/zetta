import uuid
from pydantic import BaseModel
from app.schemas.user_schemas import UserReturn


class RegisterResponse(BaseModel):
    msg: str
    usuario: UserReturn


class LoginRequest(BaseModel):
    nombre: str
    contraseña: str


class TokenData(BaseModel):
    id: uuid.UUID
    nombre: str
    correo: str
