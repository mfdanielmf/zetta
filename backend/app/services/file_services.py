from pathlib import Path
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.exceptions import TamañoExcedidoException, ArchivoNoEncontradoException, IdYaUsadaException
from app.models.file import File
from app.models.user import User
from app.repositories.file_repo import insert_file_db, get_file_by_id, get_files_user

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
TAMAÑO_LIMITE = 1000 * 1024 * 1024  # Lo limito a 1GB de momento


def obtener_archivo_id(id: uuid.UUID, db: Session) -> File:
    """
    ArchivoNoEncontradoException
    """
    archivo: File | None = get_file_by_id(id=id, db=db)

    if not archivo:
        raise ArchivoNoEncontradoException(
            f"No se ha encontrado el archivo con id {id}")

    return archivo


async def guardar_archivo(file_upload: UploadFile, db: Session, usuario: User) -> File:
    """
    TamañoExcedidoException, IdYaUsadaException
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
    IdYaUsadaException
    """
    id: uuid.UUID = uuid.uuid4()

    # Por si se genera un UUID ya usado
    if (get_file_by_id(id=id, db=db)):
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
