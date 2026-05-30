from typing import Literal, Union

from pydantic import BaseModel

from app.schemas.favorite_schemas import FavoriteFileBase, FavoriteFolderBase
from app.schemas.file_schemas import FileBase
from app.schemas.folder_schemas import FolderBase
from app.schemas.shared_file_schemas import ArchivoCompartidoBase
from app.schemas.shared_folder_schemas import CarpetaCompartidaBase


class FileItem(FileBase):
    tipo: Literal["file"] = "file"
    favorito: bool = False


class FolderItem(FolderBase):
    tipo: Literal["folder"] = "folder"
    favorito: bool = False


class SharedFileItem(ArchivoCompartidoBase):
    tipo: Literal["file"] = "file"
    favorito: bool = False


class SharedFolderItem(CarpetaCompartidaBase):
    tipo: Literal["folder"] = "folder"
    favorito: bool = False


class PaginatedItemResponse(BaseModel):
    items: list[Union[FolderItem, FileItem]]
    total: int
    pagina: int
    limite: int


class PaginatedSharedItemResponse(BaseModel):
    items: list[Union[SharedFolderItem, SharedFileItem]]
    total: int
    pagina: int
    limite: int


class PaginatedFavoriteItemReponse(BaseModel):
    items: list[Union[FavoriteFolderBase, FavoriteFileBase]]
    total: int
    pagina: int
    limite: int
