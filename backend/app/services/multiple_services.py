import os
import shutil
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.models import exceptions as ex
from app.services import file_services, folder_services
from app.repositories import file_repo, folder_repo, multiple_repo
from app.schemas import multiple_schemas


def eliminar_multiples_archivos_permanente(ids: list[UUID], usuario: User, db: Session):
    """
    ArchivoNoEncontradoException, EliminarDiscoException
    """
    errores = []

    for id_archivo in ids:
        nombre_archivo = "desconocido"

        try:
            archivo: File = file_services.obtener_archivo_papelera(
                id_archivo=id_archivo,
                usuario=usuario,
                db=db
            )

            nombre_archivo = archivo.nombre_original or "desconocido"

            path: str = archivo.path

            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    raise ex.EliminarDiscoException(
                        "Error al eliminar el archivo del disco"
                    )

            multiple_repo.delete_file(archivo=archivo, db=db)

        except Exception as e1:
            errores.append({
                "id_item": str(id_archivo),
                "nombre_item": nombre_archivo,
                "error": str(e1)
            })

    db.commit()

    return errores


def añadir_multiples_archivos_papelera(ids: list[UUID], usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException, ArchivoPapeleraException
    """
    errores = []

    for id_archivo in ids:
        nombre_archivo = "desconocido"

        try:
            if file_repo.get_file_trash(id_archivo=id_archivo, id_usuario=usuario.id, db=db):
                raise ex.ArchivoPapeleraException(
                    f"El archivo ya está en la papelera")

            archivo: File = file_services.obtener_archivo_id(
                id=id_archivo, db=db, usuario=usuario)

            nombre_archivo = archivo.nombre_original or "desconocido"

            archivo.fecha_eliminacion = datetime.now(timezone.utc)

            file_repo.update_file(archivo=archivo, db=db)

        except Exception as e1:
            errores.append({
                "id_item": str(id_archivo),
                "nombre_item": nombre_archivo,
                "error": str(e1)
            })

    return errores


def restaurar_multiples_archivos_papelera(ids: list[UUID], usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    errores = []

    for id_archivo in ids:
        nombre_archivo = "desconocido"

        try:
            archivo: File = file_services.obtener_archivo_papelera(
                id_archivo=id_archivo, db=db, usuario=usuario)

            nombre_archivo = archivo.nombre_original or "desconocido"

            archivo.fecha_eliminacion = None

            file_repo.update_file(archivo=archivo, db=db)

        except Exception as e1:
            errores.append({
                "id_item": str(id_archivo),
                "nombre_item": nombre_archivo,
                "error": str(e1)
            })

    return errores


def eliminar_multiples_carpetas_permanente(ids: list[UUID], usuario: User, db: Session):
    """
    CarpetaNoEncontradaException
    """
    errores = []

    for id_carpeta in ids:
        nombre_carpeta = "desconocida"

        try:
            carpeta: Folder = folder_services.obtener_carpeta_papelera(
                id_carpeta=id_carpeta, usuario=usuario, db=db)

            nombre_carpeta = carpeta.nombre or "desconocida"

            path: str = carpeta.path

            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                except Exception:
                    raise ex.EliminarDiscoException(
                        "Error al eliminar la carpeta del disco")

            multiple_repo.delete_folder(carpeta=carpeta, db=db)

        except Exception as e1:
            errores.append({
                "id_item": str(id_carpeta),
                "nombre_item": nombre_carpeta,
                "error": str(e1)
            })

    db.commit()

    return errores


def añadir_multiples_items_papelera(items: multiple_schemas.ItemMultipleRequest, usuario: User, db: Session):
    errores = []

    fecha_actual = datetime.now(timezone.utc)

    for item in items:
        nombre_item = "desconocido"

        try:
            if item.tipo == "archivo":

                if file_repo.get_file_trash(id_archivo=item.id, id_usuario=usuario.id, db=db):
                    raise ex.ArchivoPapeleraException(
                        "El archivo ya está en la papelera")

                archivo: File = file_services.obtener_archivo_id(
                    id=item.id, usuario=usuario, db=db)

                nombre_item = archivo.nombre_original or "desconocido"

                archivo.fecha_eliminacion = fecha_actual

                file_repo.update_file(archivo=archivo, db=db)

            else:
                if folder_repo.get_folder_trash(id_carpeta=item.id, id_usuario=usuario.id, db=db):
                    raise ex.CarpetaPapeleraException(
                        "La carpeta ya está en la papelera")

                carpeta: Folder = folder_services.obtener_carpeta_usuario_id(
                    id_carpeta=item.id, usuario=usuario, db=db)

                nombre_item = carpeta.nombre_original or "desconocida"

                path_padre = carpeta.path

                carpeta.fecha_eliminacion = fecha_actual

                db.query(Folder).filter(
                    Folder.id_usuario == usuario.id,
                    or_(
                        Folder.path == path_padre,
                        Folder.path.like(f"{path_padre}/%")
                    )
                ).update(
                    {Folder.fecha_eliminacion: fecha_actual},
                    synchronize_session=False
                )

                db.query(File).filter(
                    File.id_usuario == usuario.id,
                    File.path.like(f"{path_padre}/%")
                ).update(
                    {File.fecha_eliminacion: fecha_actual},
                    synchronize_session=False
                )

        except Exception as e1:
            errores.append({
                "id_item": str(item.id),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    db.commit()

    return errores


def eliminar_multiples_items_permanente(items: multiple_schemas.ItemMultipleRequest, usuario: User, db: Session):
    errores = []

    for item in items:
        nombre_item = "desconocido"

        try:
            if item.tipo == "archivo":

                archivo: File = file_services.obtener_archivo_papelera(
                    id_archivo=item.id, usuario=usuario, db=db)

                nombre_item = archivo.nombre_original or "desconocido"

                if os.path.exists(archivo.path):
                    os.remove(archivo.path)

                multiple_repo.delete_file(archivo=archivo, db=db)

            else:
                carpeta: Folder = folder_services.obtener_carpeta_papelera(
                    id_carpeta=item.id, usuario=usuario, db=db)

                nombre_item = carpeta.nombre or "desconocida"

                if os.path.exists(carpeta.path):
                    shutil.rmtree(carpeta.path)

                multiple_repo.delete_folder(carpeta=carpeta, db=db)

        except Exception as e1:
            errores.append({
                "id_item": str(item.id),
                "nombre_item": nombre_item,
                "error": str(e1)
            })

    db.commit()

    return errores
