from typing import Union
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.archivo_compartido import ArchivoCompartido
from app.models.carpeta_compartida import CarpetaCompartida
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.repositories import file_repo, folder_repo, shared_file_repo, shared_folder_repo
from app.services import folder_services


def obtener_items_raiz_paginados(usuario: User, db: Session, pagina: int, limite: int, busqueda: str | None) -> tuple[int, list[Union[Folder, File]]]:
    offset: int = (pagina - 1) * limite

    carpetas: list[Folder] = folder_repo.get_folders_user_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)
    archivos: list[File] = file_repo.get_files_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)

    items: list[Union[Folder, File]] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados


def obtener_items_carpeta_paginados(id_carpeta: UUID, usuario: User, db: Session, pagina: int, limite: int, busqueda: str | None) -> tuple[int, list[Union[Folder, File]]]:
    """
    CarpetaNoEncontradaException
    """
    offset: int = (pagina - 1) * limite

    folder_services.obtener_carpeta_usuario_permisos(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    carpetas: list[Folder] = folder_repo.get_folders_inside_folder_sorted(
        id_carpeta=id_carpeta, id_usuario=usuario.id, db=db, busqueda=busqueda)
    archivos: list[File] = file_repo.get_all_files_in_folder_sorted(id_carpeta=id_carpeta,
                                                                    id_usuario=usuario.id, db=db, busqueda=busqueda)

    items: list[Union[Folder, File]] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados


def obtener_items_papelera_paginados(usuario: User, db: Session, pagina: int, limite: int, busqueda: str | None) -> tuple[int, list[Union[Folder, File]]]:
    offset: int = (pagina - 1) * limite

    carpetas: list[Folder] = folder_repo.get_all_folders_trash_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)
    archivos: list[File] = file_repo.get_all_files_trash_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)

    items: list[Union[Folder, File]] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados


def obtener_items_carpeta_papelera_paginados(id_carpeta: UUID, usuario: User, db: Session, pagina: int, limite: int, busqueda: str | None) -> tuple[int, list[Union[Folder, File]]]:
    """
    CarpetaNoEncontradaException
    """
    offset: int = (pagina - 1) * limite

    folder_services.obtener_carpeta_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    carpetas: list[Folder] = folder_repo.get_folders_inside_folder_trash_sorted(
        id_carpeta=id_carpeta, id_usuario=usuario.id, db=db, busqueda=busqueda)
    archivos: list[File] = file_repo.get_all_files_in_folder_trash_sorted(id_carpeta=id_carpeta,
                                                                    id_usuario=usuario.id, db=db, busqueda=busqueda)

    items: list[Union[Folder, File]] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados


def obtener_items_compartidos_paginados(usuario: User, db: Session, pagina: int, limite: int, busqueda: str | None) -> tuple[int, list[Union[CarpetaCompartida, ArchivoCompartido]]]:
    offset: int = (pagina - 1) * limite

    carpetas: list[CarpetaCompartida] = shared_folder_repo.get_all_shared_folders_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)
    archivos: list[ArchivoCompartido] = shared_file_repo.get_all_shared_files_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)

    items: list[Union[CarpetaCompartida, ArchivoCompartido]
                ] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados


def obtener_items_recibidos_paginados(usuario: User, db: Session, pagina: int, limite: int, busqueda: str | None) -> tuple[int, list[Union[CarpetaCompartida, ArchivoCompartido]]]:
    offset: int = (pagina - 1) * limite

    carpetas: list[CarpetaCompartida] = shared_folder_repo.get_all_received_folders_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)
    archivos: list[ArchivoCompartido] = shared_file_repo.get_all_received_files_raiz_sorted(
        id_usuario=usuario.id, db=db, busqueda=busqueda)

    items: list[Union[CarpetaCompartida, ArchivoCompartido]
                ] = carpetas + archivos

    total: int = len(items)

    items_paginados = items[offset: offset + limite]

    return total, items_paginados
