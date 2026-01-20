from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator


class UserCreate(BaseModel):
    nombre: str = Field(min_length=6, max_length=20)
    correo: EmailStr = Field(max_length=120)
    contraseña: str = Field(min_length=6)
    contraseña_repetir: str = Field(min_length=6)

    @field_validator("contraseña_repetir", mode="after")
    @classmethod
    def comprobar_contraseñas_coinciden(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data["contraseña"]:
            raise ValueError('Las contraseñas no coinciden')
        return value
