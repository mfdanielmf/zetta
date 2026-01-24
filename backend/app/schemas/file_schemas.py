import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nombre_original: str
    path: str
    fecha_creacion: datetime
    id_usuario: uuid.UUID


class FileResponse(BaseModel):
    msg: str
    archivo: FileBase
