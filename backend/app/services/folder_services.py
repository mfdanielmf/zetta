from pathlib import Path
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config import config
from app.models.exceptions import IdYaUsadaException, NombreYaUsadoException, CarpetaNoEncontradaException, TamañoExcedidoException
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.repositories.folder_repo import add_folder, get_folder_id_user, get_folder_original_name, get_folders_user, get_folder_name_anidada, get_folder_id, get_folders_user_raiz
from app.repositories.file_repo import insert_file_db, get_file_by_name_in_folder

UPLOAD_DIR = Path(config.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)
TAMAÑO_LIMITE = config.TAMAÑO_LIMITE


def crear_carpeta(nombre: str, usuario: User, db: Session) -> Folder:
    """
    IdYaUsadaException, NombreYaUsadoException
    """
    if get_folder_original_name(nombre_original=nombre, usuario=usuario, db=db) is not None:
        raise NombreYaUsadoException(
            f"Ya has creado una carpeta con el nombre {nombre}")

    id_carpeta: uuid.UUID = uuid.uuid4()

    if get_folder_id(id=id_carpeta, db=db) is not None:
        raise IdYaUsadaException(
            f"Ya se ha usado la ID {id}. Vuelve a subir la carpeta")

    # Crear el almacén del usuario si no existe
    ruta_usuario = UPLOAD_DIR / str(usuario.id)
    ruta_usuario.mkdir(parents=True, exist_ok=True)

    folder_path = ruta_usuario / str(id_carpeta)
    folder_path.mkdir()

    carpeta: Folder = Folder(id=id_carpeta, nombre_original=nombre, path=str(
        folder_path), id_usuario=usuario.id)
    carpeta_db: Folder = add_folder(carpeta=carpeta, db=db)

    return carpeta_db


def obtener_carpetas_usuario(usuario: User, db: Session) -> list[Folder]:
    return get_folders_user(id_usuario=usuario.id, db=db)


def obtener_carpetas_usuario_raiz(usuario: User, db: Session) -> list[Folder]:
    return get_folders_user_raiz(id_usuario=usuario.id, db=db)


def obtener_carpeta_usuario_id(id_carpeta: str, usuario: User, db: Session) -> Folder:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = get_folder_id_user(id=id_carpeta, db=db, usuario=usuario)

    if not carpeta:
        raise CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

    return carpeta


def subir_archivo_carpeta_disco(file_path: str, data: bytes):
    """
    CarpetaNoEncontradaException
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("wb") as f:
        f.write(data)

    return


async def guardar_archivo_carpeta(id_carpeta: str, file_upload: UploadFile, db: Session, usuario: User) -> File:
    """
    TamañoExcedidoException, CarpetaNoEncontradaException, NombreYaUsadoException
    """
    carpeta: Folder = obtener_carpeta_usuario_id(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    if not carpeta:
        raise CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

    file_db: File | None = get_file_by_name_in_folder(
        nombre_original=file_upload.filename, id_carpeta=carpeta.id, usuario=usuario, db=db)

    if file_db:
        raise NombreYaUsadoException(
            f"Ya existe un archivo con el nombre '{file_upload.filename}' en la carpeta '{carpeta.nombre_original}'")

    data = await file_upload.read()

    if len(data) > TAMAÑO_LIMITE:
        raise TamañoExcedidoException(
            f"Has excedido el tamaño máximo de subida")

    id_file: uuid.UUID = uuid.uuid4()
    nombre_original = file_upload.filename

    extension = nombre_original.split(".").pop()

    ruta_usuario = UPLOAD_DIR / str(usuario.id)
    ruta_usuario.mkdir(parents=True, exist_ok=True)

    file_path = ruta_usuario / str(id_carpeta) / f"{str(id_file)}.{extension}"

    archivo: File = File(id=id_file, nombre_original=nombre_original,
                         path=str(file_path), id_usuario=usuario.id, tamaño_bytes=len(data), id_carpeta=id_carpeta)

    archivo_guardado: File = insert_file_db(archivo=archivo, db=db)

    subir_archivo_carpeta_disco(file_path=file_path, data=data)

    return archivo_guardado


def crear_carpeta_anidada(id_carpeta_padre: str, nombre: str, usuario: User, db: Session) -> Folder:
    """
    CarpetaNoEncontradaException, NombreYaUsadoException, IdYaUsadaException
    """
    if not get_folder_id_user(id=id_carpeta_padre, usuario=usuario, db=db):
        raise CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con ID {id_carpeta_padre}")

    if get_folder_name_anidada(id_carpeta_padre=id_carpeta_padre, nombre_carpeta=nombre, usuario=usuario, db=db):
        raise NombreYaUsadoException(
            f"Ya has creado una carpeta con el nombre {nombre}")

    id_carpeta_nueva: uuid.UUID = uuid.uuid4()

    if get_folder_id(id_carpeta=id_carpeta_nueva, db=db) is not None:
        raise IdYaUsadaException(
            f"Ya se ha usado la ID {id}. Vuelve a crear la carpeta")

    # Crear el almacén del usuario si no existe
    ruta_usuario = UPLOAD_DIR / str(usuario.id)
    ruta_usuario.mkdir(parents=True, exist_ok=True)

    folder_path = ruta_usuario / str(id_carpeta_padre) / str(id_carpeta_nueva)
    folder_path.mkdir()

    carpeta: Folder = Folder(id=id_carpeta_nueva, nombre_original=nombre, path=str(
        folder_path), id_usuario=usuario.id, id_carpeta=id_carpeta_padre)
    carpeta_db: Folder = add_folder(carpeta=carpeta, db=db)

    return carpeta_db
