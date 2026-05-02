from datetime import datetime, timezone
import os
from pathlib import Path
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models import exceptions as ex
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.repositories import shared_file_repo
from app.repositories import file_repo
from app.services import folder_services

from app.config import config

UPLOAD_DIR = Path(config.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)
TAMAÑO_LIMITE = config.TAMAÑO_LIMITE  # Lo limito a 1GB de momento


def obtener_archivo_id(id: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File | None = file_repo.get_file_by_id_and_user(
        id=id, usuario=usuario, db=db)

    if not archivo:
        raise ex.ArchivoNoEncontradoException(
            f"No se ha encontrado el archivo con id {id}")

    return archivo


def obtener_archivo_papelera(id_archivo: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File | None = file_repo.get_file_trash(
        id_archivo=id_archivo, id_usuario=usuario.id, db=db)

    if not archivo:
        raise ex.ArchivoNoEncontradoException(
            f"No se ha encontrado el archivo con id {id_archivo}")

    return archivo


def obtener_archivos_papelera_raiz(usuario: User, db: Session) -> list[File]:
    return file_repo.get_all_files_trash_raiz(id_usuario=usuario.id, db=db)


async def guardar_archivo(file_upload: UploadFile, db: Session, usuario: User) -> File:
    """
    TamañoExcedidoException, IdYaUsadaException, NombreYaUsadoException
    """
    data = await file_upload.read()

    if len(data) > TAMAÑO_LIMITE:
        raise ex.TamañoExcedidoException(
            f"Has excedido el tamaño máximo de subida")

    archivo_db, file_path = añadir_archivo_db(
        nombre_original=file_upload.filename, db=db, usuario=usuario, tamaño=len(data))

    with file_path.open("wb") as f:
        f.write(data)

    return archivo_db


def añadir_archivo_db(nombre_original: str, tamaño: int, db: Session, usuario: User) -> tuple[File, str]:
    """
    IdYaUsadaException, NombreYaUsadoException
    """

    # Si hay un archivo con el mismo nombre en la raiz (no tiene id_carpeta), salimos
    if file_repo.get_file_by_name_in_folder(nombre_original=nombre_original, usuario=usuario, db=db):
        raise ex.NombreYaUsadoException(
            f"Ya hay un archivo con el nombre '{nombre_original}'. Cambia el nombre")

    id: uuid.UUID = uuid.uuid4()

    # Por si se genera un UUID ya usado
    if file_repo.get_file_by_id(id_archivo=id, db=db):
        raise ex.IdYaUsadaException(
            f"Ya se ha usado la ID {id}. Vuelve a subir el archivo")

    extension = nombre_original.split(".").pop()  # png, jpg, txt...

    # Crear la carpeta si no existe
    ruta_usuario = UPLOAD_DIR / str(usuario.id)
    ruta_usuario.mkdir(parents=True, exist_ok=True)

    file_path = ruta_usuario / f"{str(id)}.{extension}"

    archivo: File = File(id=id, nombre_original=nombre_original,
                         path=str(file_path), id_usuario=usuario.id, tamaño_bytes=tamaño)

    archivo_db: File = file_repo.insert_file_db(archivo=archivo, db=db)

    return archivo_db, file_path


def obtener_archivos_usuario(usuario: User, db: Session) -> list[File]:
    return file_repo.get_files_raiz(id_usuario=usuario.id, db=db)


def obtener_archivos_carpeta(id_carpeta: uuid.UUID, db: Session, usuario: User) -> list[File]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = folder_services.obtener_carpeta_usuario_permisos(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    return carpeta.archivos


def añadir_archivo_papelera(id_archivo: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException, ArchivoPapeleraException
    """
    if file_repo.get_file_trash(id_archivo=id_archivo, id_usuario=usuario.id, db=db):
        raise ex.ArchivoPapeleraException()

    archivo: File = obtener_archivo_id(id=id_archivo, db=db, usuario=usuario)
    archivo.fecha_eliminacion = datetime.now(timezone.utc)

    return file_repo.update_file(archivo=archivo, db=db)


def restaurar_archivo_papelera(id_archivo: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File = obtener_archivo_papelera(
        id_archivo=id_archivo, db=db, usuario=usuario)
    archivo.fecha_eliminacion = None

    return file_repo.update_file(archivo=archivo, db=db)


def obtener_archivos_carpeta_papelera(id_carpeta: uuid.UUID, usuario: User, db: Session) -> list[File]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = folder_services.obtener_carpeta_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    return carpeta.archivos


def eliminar_archivo_permanente(id_archivo: uuid.UUID, usuario: User, db: Session):
    """
    ArchivoNoEncontradoException, EliminarDiscoException
    """
    archivo: File = obtener_archivo_papelera(
        id_archivo=id_archivo, usuario=usuario, db=db)

    path: str = archivo.path

    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        raise ex.EliminarDiscoException("Error al eliminar el archivo del disco")

    file_repo.delete_file(archivo=archivo, db=db)


def obtener_archivo_permisos(id_archivo: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File | None = file_repo.get_file_by_id(id_archivo=id_archivo, db=db)

    if not archivo:
        raise ex.ArchivoNoEncontradoException(
            f"No se ha encontrado el archivo con id {id}")

    if archivo.id_usuario == usuario.id:
        return archivo

    if shared_file_repo.get_shared_file(id_archivo=id_archivo, id_receptor=usuario.id, db=db):
        return archivo

    # Miramos si el archivo está dentro de una carpeta compartida
    try:
        if archivo.id_carpeta:
            folder_services.obtener_carpeta_usuario_permisos(
                id_carpeta=archivo.id_carpeta, usuario=usuario, db=db)

            # Si la carpeta no lanza excepción, tiene permisos
            return archivo
    except ex.CarpetaNoEncontradaException:
        raise ex.ArchivoNoEncontradoException(
            f"No se ha encontrado el archivo con id {id_archivo}")

    raise ex.ArchivoNoEncontradoException(
        f"No se ha encontrado el archivo con id {id_archivo}")

def obtener_archivos_usuario_paginados(usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[File]]:
    offset: int = (pagina - 1) * limite

    return file_repo.get_files_raiz_paginados(id_usuario=usuario.id, db=db, offset=offset, limit=limite)