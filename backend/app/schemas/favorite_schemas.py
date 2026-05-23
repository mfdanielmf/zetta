from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.file_schemas import FileBase
from app.schemas.folder_schemas import FolderBase
from app.schemas.user_schemas import UserReturn


class FavoriteFolderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    fecha_favorito: datetime
    usuario: UserReturn
    carpeta: FolderBase
    tipo: Literal["folder"] = "folder"


class FavoriteFileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    fecha_favorito: datetime
    usuario: UserReturn
    archivo: FileBase
    tipo: Literal["file"] = "file"
