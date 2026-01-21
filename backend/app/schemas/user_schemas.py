from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationInfo, field_validator


class UserCreate(BaseModel):
    nombre: str = Field(min_length=4, max_length=20)
    correo: EmailStr = Field(max_length=120)
    contraseña: str = Field(min_length=6)
    contraseña_repetir: str = Field(min_length=6)

    @field_validator("contraseña_repetir", mode="after")
    @classmethod
    def comprobar_contraseñas_coinciden(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data["contraseña"]:
            raise ValueError('Las contraseñas no coinciden')
        return value


class UserReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nombre: str
    correo: str
    fecha_creacion: datetime
