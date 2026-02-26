import uuid

from sqlalchemy.orm import Session

from app.models.folder import Folder
from app.models.user import User

def add_folder(carpeta: Folder, db: Session) -> Folder:
    db.add(carpeta)
    db.commit()
    db.flush(carpeta)

    return carpeta

def get_folder_id_user(id: uuid.UUID, usuario: User, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(id=id, id_usuario=usuario.id).first()

def get_folder_original_name(nombre_original: str, usuario: User, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(nombre_original=nombre_original, id_usuario=usuario.id).first()