from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.folder_schemas import FolderBase
from app.schemas.user_schemas import UserReturn


class CarpetaCompartidaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    fecha_compartido: datetime
    propietario: UserReturn
    receptor: UserReturn
    carpeta: FolderBase


class ShareFolderRequest(BaseModel):
    id_carpeta: UUID
    correo_usuario: EmailStr


class ShareFolderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    msg: str = "Carpeta compartida con éxito"
    carpeta_compartida: CarpetaCompartidaBase
