from typing import Literal, Union

from pydantic import BaseModel

from app.schemas.file_schemas import FileBase
from app.schemas.folder_schemas import FolderBase
from app.schemas.shared_file_schemas import ArchivoCompartidoBase
from app.schemas.shared_folder_schemas import CarpetaCompartidaBase


class FileItem(FileBase):
    tipo: Literal["file"] = "file"


class FolderItem(FolderBase):
    tipo: Literal["folder"] = "folder"


class SharedFileItem(ArchivoCompartidoBase):
    tipo: Literal["file"] = "file"


class SharedFolderItem(CarpetaCompartidaBase):
    tipo: Literal["folder"] = "folder"


class PaginatedItemResponse(BaseModel):
    items: list[Union[FolderItem, FileItem]]
    total: int
    pagina: int
    limite: int


class PaginatedSharedItemResponse(BaseModel):
    items: list[Union[CarpetaCompartidaBase, ArchivoCompartidoBase]]
    total: int
    pagina: int
    limite: int
