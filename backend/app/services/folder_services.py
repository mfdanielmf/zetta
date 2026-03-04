from pathlib import Path
import uuid

from sqlalchemy.orm import Session

from app.config import config
from app.models.exceptions import IdYaUsadaException, NombreYaUsadoException
from app.models.folder import Folder
from app.models.user import User
from app.repositories.folder_repo import add_folder, get_folder_id_user, get_folder_original_name, get_folders_user

UPLOAD_DIR = Path(config.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)


def crear_carpeta(nombre: str, usuario: User, db: Session) -> Folder:
    """
    IdYaUsadaException, NombreYaUsadoException
    """
    if get_folder_original_name(nombre_original=nombre, usuario=usuario, db=db) is not None:
        raise NombreYaUsadoException(
            f"Ya has creado una carpeta con el nombre {nombre}")

    id_carpeta: uuid.UUID = uuid.uuid4()

    if get_folder_id_user(id=id_carpeta, usuario=usuario, db=db) is not None:
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
