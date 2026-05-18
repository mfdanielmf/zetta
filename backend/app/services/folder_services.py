import os
import tempfile
import zipfile
import io
import shutil
import uuid
from pathlib import Path
from datetime import datetime, timezone

from fastapi import UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import config
from app.models import exceptions as ex
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.repositories import shared_folder_repo, folder_repo, file_repo

UPLOAD_DIR = Path(config.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)
TAMAÑO_LIMITE = config.TAMANO_LIMITE


def crear_carpeta(nombre: str, usuario: User, db: Session) -> Folder:
    """
    IdYaUsadaException, NombreYaUsadoException
    """
    if folder_repo.get_folder_nombre_raiz(nombre_carpeta=nombre, id_usuario=usuario.id, db=db) is not None:
        raise ex.NombreYaUsadoException(
            f"Ya has creado una carpeta con el nombre {nombre}")

    id_carpeta: uuid.UUID = uuid.uuid4()

    if folder_repo.get_folder_id(id_carpeta=id_carpeta, db=db) is not None:
        raise ex.IdYaUsadaException(
            f"Ya se ha usado la ID {id}. Vuelve a subir la carpeta")

    # Crear el almacén del usuario si no existe
    ruta_usuario = UPLOAD_DIR / str(usuario.id)
    ruta_usuario.mkdir(parents=True, exist_ok=True)

    folder_path = ruta_usuario / str(id_carpeta)
    folder_path.mkdir(parents=True, exist_ok=True)

    carpeta: Folder = Folder(id=id_carpeta, nombre_original=nombre, path=str(
        folder_path), id_usuario=usuario.id)
    carpeta_db: Folder = folder_repo.add_folder(carpeta=carpeta, db=db)

    return carpeta_db


def obtener_carpetas_usuario(usuario: User, db: Session) -> list[Folder]:
    return folder_repo.get_folders_user(id_usuario=usuario.id, db=db)


def obtener_carpetas_usuario_raiz(usuario: User, db: Session) -> list[Folder]:
    return folder_repo.get_folders_user_raiz(id_usuario=usuario.id, db=db)


def obtener_carpetas_dentro_carpeta(id_carpeta_padre: uuid.UUID, usuario: User, db: Session) -> list[Folder]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_usuario_permisos(
        id_carpeta=id_carpeta_padre, usuario=usuario, db=db)

    return carpeta.carpetas


def obtener_carpeta_usuario_id(id_carpeta: str, usuario: User, db: Session) -> Folder:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = folder_repo.get_folder_id_user(
        id=id_carpeta, db=db, usuario=usuario)

    if not carpeta:
        raise ex.CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

    return carpeta


def obtener_carpeta_papelera(id_carpeta: uuid.UUID, usuario: User, db: Session) -> Folder:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = folder_repo.get_folder_trash(
        id_carpeta=id_carpeta, id_usuario=usuario.id, db=db)

    if not carpeta:
        raise ex.CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con ID {id_carpeta} en la papelera")

    return carpeta


def obtener_carpetas_papelera_raiz(usuario: User, db: Session) -> list[Folder]:
    return folder_repo.get_all_folders_trash_raiz(id_usuario=usuario.id, db=db)


async def guardar_archivo_carpeta(id_carpeta: str, file_upload: UploadFile, db: Session, usuario: User) -> File:
    """
    TamañoExcedidoException, CarpetaNoEncontradaException, NombreYaUsadoException
    """
    carpeta: Folder = obtener_carpeta_usuario_id(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    file_db: File | None = file_repo.get_file_by_name_in_folder(
        nombre_original=file_upload.filename, id_carpeta=carpeta.id, usuario=usuario, db=db)

    if file_db:
        raise ex.NombreYaUsadoException(
            f"Ya existe un archivo con el nombre '{file_upload.filename}' en la carpeta '{carpeta.nombre_original}'")

    id_file: uuid.UUID = uuid.uuid4()
    nombre_original = file_upload.filename

    extension: str = nombre_original.split(".").pop()

    file_path = Path(carpeta.path) / f"{str(id_file)}.{extension}"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    tamaño: int = 0

    with file_path.open("wb") as f:
        while True:
            chunk = await file_upload.read(1024 * 1024)

            if not chunk:
                break

            tamaño += len(chunk)

            if tamaño > TAMAÑO_LIMITE:
                file_path.unlink(missing_ok=True)

                raise ex.TamañoExcedidoException(
                    "Has excedido el tamaño máximo de subida")

            f.write(chunk)

    archivo: File = File(id=id_file, nombre_original=nombre_original,
                         path=str(file_path), id_usuario=usuario.id, tamaño_bytes=tamaño, id_carpeta=id_carpeta)

    archivo_guardado: File = file_repo.insert_file_db(archivo=archivo, db=db)

    return archivo_guardado


def crear_carpeta_anidada(id_carpeta_padre: str, nombre: str, usuario: User, db: Session) -> Folder:
    """
    CarpetaNoEncontradaException, NombreYaUsadoException, IdYaUsadaException
    """
    carpeta_padre: Folder | None = folder_repo.get_folder_id_user(
        id=id_carpeta_padre, usuario=usuario, db=db)

    if not carpeta_padre:
        raise ex.CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con ID {id_carpeta_padre}")

    if folder_repo.get_folder_name_anidada(id_carpeta_padre=id_carpeta_padre, nombre_carpeta=nombre, usuario=usuario, db=db):
        raise ex.NombreYaUsadoException(
            f"Ya has creado una carpeta con el nombre {nombre}")

    id_carpeta_nueva: uuid.UUID = uuid.uuid4()

    if folder_repo.get_folder_id(id_carpeta=id_carpeta_nueva, db=db) is not None:
        raise ex.IdYaUsadaException(
            f"Ya se ha usado el ID {id_carpeta_nueva}. Vuelve a crear la carpeta")

    folder_path = Path(carpeta_padre.path) / str(id_carpeta_nueva)

    folder_path.mkdir(parents=True, exist_ok=True)

    carpeta: Folder = Folder(id=id_carpeta_nueva, nombre_original=nombre, path=str(
        folder_path), id_usuario=usuario.id, id_carpeta=id_carpeta_padre)
    carpeta_db: Folder = folder_repo.add_folder(carpeta=carpeta, db=db)

    return carpeta_db


def añadir_carpeta_papelera(id_carpeta: uuid.UUID, usuario: User, db: Session) -> Folder:
    """
    CarpetaPapeleraException, CarpetaNoEncontradaException
    """
    if folder_repo.get_folder_trash(id_carpeta=id_carpeta, id_usuario=usuario.id, db=db):
        raise ex.CarpetaPapeleraException()

    carpeta: Folder = obtener_carpeta_usuario_id(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    fecha_actual = datetime.now(timezone.utc)
    path_padre: str = carpeta.path

    carpeta.fecha_eliminacion = fecha_actual

    # Actualizar todas las carpetas con el path del padre
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

    # Actualizar todos los archivos con el path del padre
    db.query(File).filter(
        File.id_usuario == usuario.id,
        File.path.like(f"{path_padre}/%")
    ).update(
        {File.fecha_eliminacion: fecha_actual},
        synchronize_session=False
    )

    return folder_repo.update_folder(carpeta=carpeta, db=db)


def restaurar_carpeta_papelera(id_carpeta: uuid.UUID, usuario: User, db: Session):
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    carpeta.fecha_eliminacion = None
    path_padre: str = carpeta.path

    # Actualizar todas las carpetas con el path del padre
    db.query(Folder).filter(
        Folder.id_usuario == usuario.id,
        or_(
            Folder.path == path_padre,
            Folder.path.like(f"{path_padre}/%")
        )
    ).update(
        {Folder.fecha_eliminacion: None},
        synchronize_session=False
    )

    # Actualizar todos los archivos con el path del padre
    db.query(File).filter(
        File.id_usuario == usuario.id,
        File.path.like(f"{path_padre}/%")
    ).update(
        {File.fecha_eliminacion: None},
        synchronize_session=False
    )

    return folder_repo.update_folder(carpeta=carpeta, db=db)


def obtener_carpetas_carpeta_papelera(id_carpeta: uuid.UUID, usuario: User, db: Session) -> list[Folder]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    return folder_repo.get_folders_inside_folder(id_carpeta=carpeta.id, id_usuario=usuario.id, db=db)


def eliminar_carpeta_permanente(id_carpeta: uuid.UUID, usuario: User, db: Session):
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    path: str = carpeta.path

    try:
        if os.path.exists(path):
            shutil.rmtree(path=path)
    except Exception:
        raise ex.EliminarDiscoException(
            "Error al eliminar la carpeta del disco")

    folder_repo.delete_folder(carpeta=carpeta, db=db)


def obtener_carpeta_usuario_permisos(id_carpeta: str, usuario: User, db: Session) -> Folder:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder | None = folder_repo.get_folder_id(
        id_carpeta=id_carpeta, db=db)

    if not carpeta:
        raise ex.CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

    # Devolvemos la carpeta si el usuario es el propietario o la carpeta está compartida con él
    if carpeta.id_usuario == usuario.id:
        return carpeta

    carpeta_actual: Folder = carpeta

    # Si la carpeta está anidada, buscamos si algún padre está compartido
    while carpeta_actual:
        if shared_folder_repo.get_shared_folder(id_carpeta=carpeta_actual.id, id_receptor=usuario.id, db=db):
            return carpeta

        # Raíz
        if not carpeta_actual.id_carpeta:
            break

        carpeta_actual = folder_repo.get_folder_id(
            id_carpeta=carpeta_actual.id_carpeta, db=db)

    raise ex.CarpetaNoEncontradaException(
        f"No se ha encontrado la carpeta con id {id_carpeta}")


def obtener_carpeta_usuario_permisos_no_papelera(id_carpeta: str, usuario: User, db: Session) -> Folder:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder | None = folder_repo.get_folder_id_no_trash(
        id_carpeta=id_carpeta, db=db)

    if not carpeta:
        raise ex.CarpetaNoEncontradaException(
            f"No se ha encontrado la carpeta con id {id_carpeta}")

    # Devolvemos la carpeta si el usuario es el propietario o la carpeta está compartida con él
    if carpeta.id_usuario == usuario.id:
        return carpeta

    carpeta_actual: Folder = carpeta

    # Si la carpeta está anidada, buscamos si algún padre está compartido
    while carpeta_actual:
        if shared_folder_repo.get_shared_folder(id_carpeta=carpeta_actual.id, id_receptor=usuario.id, db=db):
            return carpeta

        # Raíz
        if not carpeta_actual.id_carpeta:
            break

        carpeta_actual = folder_repo.get_folder_id(
            id_carpeta=carpeta_actual.id_carpeta, db=db)

    raise ex.CarpetaNoEncontradaException(
        f"No se ha encontrado la carpeta con id {id_carpeta}")


def descargar_carpeta(id_carpeta: uuid.UUID, usuario: User, db: Session) -> tuple[io.BytesIO, Folder]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_usuario_permisos_no_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    archivo_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    zip_path: str = archivo_temp.name
    archivo_temp.close()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        añadir_carpeta_a_zip(zipf=zipf, carpeta=carpeta, path_base="")

    return zip_path, carpeta


def añadir_carpeta_a_zip(zipf: zipfile.ZipFile, carpeta: Folder, path_base: str) -> None:
    path_actual: str = f"{path_base}{carpeta.nombre_original}/"

    # Crear carpeta aunque esté vacía
    zipf.writestr(path_actual, "")

    # Añadimos los archivos que tenga la carpeta al zip
    for archivo in carpeta.archivos:
        if archivo.fecha_eliminacion is None:
            zipf.write(
                archivo.path, arcname=f"{path_actual}{archivo.nombre_original}")

    # Añadimos las carpetas anidadas
    for carpeta_anidada in carpeta.carpetas:
        if carpeta_anidada.fecha_eliminacion is None:
            añadir_carpeta_a_zip(
                zipf=zipf, carpeta=carpeta_anidada, path_base=path_actual)


def obtener_carpetas_usuario_raiz_paginadas(usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[Folder]]:
    offset: int = (pagina - 1) * limite

    return folder_repo.get_folders_user_raiz_paginadas(id_usuario=usuario.id, db=db, offset=offset, limit=limite)


def obtener_carpetas_papelera_raiz_paginadas(usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[Folder]]:
    offset: int = (pagina - 1) * limite

    return folder_repo.get_all_folders_trash_raiz_paginadas(id_usuario=usuario.id, db=db, offset=offset, limit=limite)


def obtener_carpetas_carpeta_papelera_paginadas(id_carpeta: uuid.UUID, usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[Folder]]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_papelera(
        id_carpeta=id_carpeta, usuario=usuario, db=db)

    offset: int = (pagina - 1) * limite

    return folder_repo.get_folders_inside_folder_paginadas(id_carpeta=carpeta.id, id_usuario=usuario.id, db=db, offset=offset, limit=limite)


def obtener_carpetas_dentro_carpeta_paginadas(id_carpeta_padre: uuid.UUID, usuario: User, db: Session, pagina: int, limite: int) -> tuple[int, list[Folder]]:
    """
    CarpetaNoEncontradaException
    """
    carpeta: Folder = obtener_carpeta_usuario_permisos(
        id_carpeta=id_carpeta_padre, usuario=usuario, db=db)

    offset: int = (pagina - 1) * limite

    return folder_repo.get_folders_inside_folder_paginadas(id_carpeta=carpeta.id, id_usuario=usuario.id, db=db, offset=offset, limit=limite)
