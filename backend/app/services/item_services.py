from typing import Union

from sqlalchemy.orm import Session

from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.repositories import file_repo, folder_repo


def obtener_items_raiz_paginados(usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[Union[Folder, File]]]:
    offset: int = (pagina - 1) * limite

    carpetas: list[Folder] = folder_repo.get_folders_user_raiz_sorted(
        id_usuario=usuario.id, db=db)
    archivos: list[File] = file_repo.get_files_raiz_sorted(
        id_usuario=usuario.id, db=db)

    items: list[Union[Folder, File]] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados
