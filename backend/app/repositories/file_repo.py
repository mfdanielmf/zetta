import uuid
from app.models.file import File
from sqlalchemy.orm import Session

from app.models.user import User


def insert_file_db(archivo: File, db: Session) -> File:
    db.add(archivo)
    db.commit()
    db.flush(archivo)

    return archivo


def get_file_by_id_and_user(id: uuid.UUID, usuario: User, db: Session) -> File | None:
    return db.query(File).filter_by(id=id, id_usuario=usuario.id).first()

def get_files_user(usuario: User, db: Session) -> list[File]:
    return db.query(File).filter_by(id_usuario=usuario.id).all()


def get_file_original_name(nombre_original: str, usuario: User, db: Session) -> File | None:
    return db.query(File).filter_by(nombre_original=nombre_original, id_usuario=usuario.id).first()
