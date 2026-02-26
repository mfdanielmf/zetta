from pathlib import Path
import uuid

from sqlalchemy.orm import Session

from app.config import config
from app.models.folder import Folder
from app.models.user import User
from app.repositories.folder_repo import add_folder

UPLOAD_DIR = Path(config.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)

def crear_carpeta(nombre: str, usuario: User, db: Session) -> Folder:
    id_carpeta: uuid.UUID = uuid.uuid4()

    # Crear el almacén del usuario si no existe
    ruta_usuario = UPLOAD_DIR / str(usuario.id)
    ruta_usuario.mkdir(parents=True, exist_ok=True)

    folder_path = ruta_usuario / str(id_carpeta)
    folder_path.mkdir()
    
    carpeta: Folder = Folder(id=id_carpeta, nombre_original=nombre, path=str(folder_path), id_usuario=usuario.id)
    carpeta_db: Folder = add_folder(carpeta=carpeta, db=db)

    return carpeta_db