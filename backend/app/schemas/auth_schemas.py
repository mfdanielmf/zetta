from pydantic import BaseModel
from app.schemas.user_schemas import UserReturn


class RegisterResponse(BaseModel):
    msg: str
    usuario: UserReturn
