from datetime import datetime, timezone
from pathlib import Path
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.exceptions import ArchivoPapeleraException, TamañoExcedidoException, ArchivoNoEncontradoException, IdYaUsadaException, NombreYaUsadoException
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.repositories.file_repo import insert_file_db, get_file_by_id_and_user, get_files_user, get_file_by_name_in_folder, get_all_files_in_folder, update_file, get_file_trash, get_all_files_trash_raiz

from app.config import config
from app.services.folder_services import obtener_carpeta_usuario_id, obtener_carpeta_papelera

UPLOAD_DIR = Path(config.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)
TAMAÑO_LIMITE = config.TAMAÑO_LIMITE  # Lo limito a 1GB de momento


def obtener_archivo_id(id: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File | None = get_file_by_id_and_user(
        id=id, usuario=usuario, db=db)

    if not archivo:
        raise ArchivoNoEncontradoException(
            f"No se ha encontrado el archivo con id {id}")

    return archivo


def obtener_archivo_papelera(id_archivo: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File | None = get_file_trash(
        id_archivo=id_archivo, id_usuario=usuario.id, db=db)

    if not archivo:
        raise ArchivoNoEncontradoException(
            f"No se ha encontrado el archivo con id {id}")

    return archivo


def obtener_archivos_papelera_raiz(usuario: User, db: Session) -> list[File]:
    return get_all_files_trash_raiz(id_usuario=usuario.id, db=db)


async def guardar_archivo(file_upload: UploadFile, db: Session, usuario: User) -> File:
    """
    TamañoExcedidoException, IdYaUsadaException, NombreYaUsadoException
    """
    data = await file_upload.read()

    if len(data) > TAMAÑO_LIMITE:
        raise TamañoExcedidoException(
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
    if get_file_by_name_in_folder(nombre_original=nombre_original, usuario=usuario, db=db):
        raise NombreYaUsadoException(
            f"Ya hay un archivo con el nombre '{nombre_original}'. Cambia el nombre")

    id: uuid.UUID = uuid.uuid4()

    # Por si se genera un UUID ya usado
    if get_file_by_id_and_user(id=id, usuario=usuario, db=db):
        raise IdYaUsadaException(
            f"Ya se ha usado la ID {id}. Vuelve a subir el archivo")

    extension = nombre_original.split(".").pop()  # png, jpg, txt...

    # Crear la carpeta si no existe
    ruta_usuario = UPLOAD_DIR / str(usuario.id)
    ruta_usuario.mkdir(parents=True, exist_ok=True)

    file_path = ruta_usuario / f"{str(id)}.{extension}"

    archivo: File = File(id=id, nombre_original=nombre_original,
                         path=str(file_path), id_usuario=usuario.id, tamaño_bytes=tamaño)

    archivo_db: File = insert_file_db(archivo=archivo, db=db)

    return archivo_db, file_path


def obtener_archivos_usuario(usuario: User, db: Session) -> list[File]:
    return get_files_user(usuario=usuario, db=db)


def obtener_archivos_carpeta(id_carpeta: uuid.UUID, db: Session, usuario: User) -> list[File]:
    """
    CarpetaNoEncontradaException
    """
    obtener_carpeta_usuario_id(id_carpeta=id_carpeta, usuario=usuario, db=db)

    return get_all_files_in_folder(db=db, id_carpeta=id_carpeta, usuario=usuario)


def añadir_archivo_papelera(id_archivo: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException, ArchivoPapeleraException
    """
    if get_file_trash(id_archivo=id_archivo, id_usuario=usuario.id, db=db):
        raise ArchivoPapeleraException()

    archivo: File = obtener_archivo_id(id=id_archivo, db=db, usuario=usuario)
    archivo.fecha_eliminacion = datetime.now(timezone.utc)

    return update_file(archivo=archivo, db=db)


def restaurar_archivo_papelera(id_archivo: uuid.UUID, usuario: User, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File = obtener_archivo_papelera(
        id_archivo=id_archivo, db=db, usuario=usuario)
    archivo.fecha_eliminacion = None

    return update_file(archivo=archivo, db=db)


def obtener_archivos_carpeta_papelera(id_carpeta: uuid.UUID, usuario: User, db: Session) -> list[File]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    return carpeta.archivos
