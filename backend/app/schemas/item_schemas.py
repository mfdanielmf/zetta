from typing import Literal, Union

from pydantic import BaseModel

from app.schemas.file_schemas import FileBase
from app.schemas.folder_schemas import FolderBase


class FileItem(FileBase):
    tipo: Literal["file"] = "file"


class FolderItem(FolderBase):
    tipo: Literal["folder"] = "folder"


class PaginatedItemResponse(BaseModel):
    items: list[Union[FolderItem, FileItem]]
    total: int
    pagina: int
    limite: int
