from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.folder import Folder

class FolderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nombre_original: str
    path: str
    fecha_creacion: datetime
    id_usuario: uuid.UUID
    nombre_usuario: str


class FolderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    msg: str
    carpeta: FolderBase