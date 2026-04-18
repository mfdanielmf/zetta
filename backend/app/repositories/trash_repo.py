
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.file import File
from app.models.folder import Folder


def get_folders_trash_delete(db: Session, limite_papelera: datetime) -> list[Folder]:
    return db.query(Folder).filter(Folder.fecha_eliminacion.isnot(None)).filter(Folder.fecha_eliminacion < limite_papelera).all()


def get_files_trash_delete(db: Session, limite_papelera: datetime) -> list[File]:
    return db.query(File).filter(File.fecha_eliminacion.isnot(None)).filter(File.fecha_eliminacion < limite_papelera).all()
