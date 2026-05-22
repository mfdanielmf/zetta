from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.file_schemas import FileBase


class FolderRequest(BaseModel):
    nombre_carpeta: str


class FolderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nombre_original: str
    path: str
    fecha_creacion: datetime
    favorito: bool = False
    id_usuario: uuid.UUID
    nombre_usuario: str
    id_carpeta: uuid.UUID | None = None
    fecha_eliminacion: datetime | None = None
    fecha_favorito: datetime | None = None


class FolderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    msg: str
    carpeta: FolderBase


class UploadFileFolderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    msg: str
    archivos: list[FileBase]


class AddFolderTrashResponse(FolderResponse):
    pass


class RestoreFolderResponse(FolderResponse):
    pass


class DeleteFolderPermanentResponse(BaseModel):
    msg: str = "Carpeta eliminada correctamente"


class PaginatedFolderResponse(BaseModel):
    items: list[FolderBase]
    total: int
    pagina: int
    limite: int
