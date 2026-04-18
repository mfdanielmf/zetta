from datetime import datetime, timedelta, timezone
import os
import shutil

from sqlalchemy.orm import Session
from app.config import config
from app.models.exceptions import EliminarDiscoException
from app.models.file import File
from app.models.folder import Folder
from app.repositories import trash_repo, file_repo, folder_repo


def _get_limit_papelera() -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=config.DIAS_PAPELERA)


def eliminar_data_papelera(db: Session):
    """
    EliminarDiscoException
    """
    limite_papelera: datetime = _get_limit_papelera()

    try:
        # Borrar carpetas disco
        carpetas_eliminar: list[Folder] = trash_repo.get_folders_trash_delete(
            db=db, limite_papelera=limite_papelera)

        for carpeta in carpetas_eliminar:
            path: str = carpeta.path

            if os.path.exists(path):
                shutil.rmtree(path=path)

        # Borrar archivos disco
        archivos_eliminar: list[File] = trash_repo.get_files_trash_delete(
            db=db, limite_papelera=limite_papelera)

        for archivo in archivos_eliminar:
            path: str = archivo.path

            if os.path.exists(path):
                os.remove(path)
    except Exception:
        raise EliminarDiscoException("Error al eliminar datos del disco")

    # Borrar de db si todo va bien
    for carpeta_db in carpetas_eliminar:
        folder_repo.delete_folder(carpeta=carpeta_db, db=db)

    for archivo_db in archivos_eliminar:
        file_repo.delete_file(archivo=archivo_db, db=db)
