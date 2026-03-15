import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nombre_original: str
    path: str
    fecha_creacion: datetime
    tamaño_bytes: int
    id_usuario: uuid.UUID
    id_carpeta: uuid.UUID | None
    nombre_usuario: str


class FileResponse(BaseModel):
    msg: str
    archivos: list[FileBase]
