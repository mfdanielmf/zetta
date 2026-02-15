import uuid
from app.models.file import File
from sqlalchemy.orm import Session

from app.models.user import User


def insert_file_db(archivo: File, db: Session) -> File:
    db.add(archivo)
    db.commit()
    db.flush(archivo)

    return archivo


def get_file_by_id(id: uuid.UUID, db: Session) -> File | None:
    archivo: File | None = db.get(File, id)

    return archivo


def get_files_user(usuario: User, db: Session) -> list[File]:
    return db.query(File).filter_by(id_usuario=usuario.id).all()
