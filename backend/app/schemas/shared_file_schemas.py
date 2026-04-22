from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.file_schemas import FileBase
from app.schemas.user_schemas import UserReturn


class ArchivoCompartidoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    fecha_compartido: datetime
    propietario: UserReturn
    receptor: UserReturn
    archivo: FileBase


class ShareFileRequest(BaseModel):
    id_archivo: UUID
    correo_usuario: EmailStr


class ShareFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    msg: str
    archivo_compartido: ArchivoCompartidoBase
