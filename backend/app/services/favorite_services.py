from typing import Union

from sqlalchemy.orm import Session

from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.repositories import favorite_repo


def obtener_items_favoritos(db: Session, usuario: User, pagina: int, limite: int, busqueda: str | None) -> tuple[int, list[Union[Folder, File]]]:
    offset: int = (pagina - 1) * limite

    carpetas: list[Folder] = favorite_repo.get_favorite_folders(
        id_usuario=usuario.id, db=db, busqueda=busqueda)
    archivos: list[File] = favorite_repo.get_favorite_files(
        id_usuario=usuario.id, db=db, busqueda=busqueda)

    items: list[Union[Folder, File]] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados
