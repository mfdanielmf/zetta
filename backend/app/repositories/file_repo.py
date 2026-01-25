import uuid
from app.models.file import File
from sqlalchemy.orm import Session


def insert_file_db(archivo: File, db: Session) -> File:
    db.add(archivo)
    db.commit()
    db.flush(archivo)

    return archivo


def get_file_by_id(id: uuid.UUID, db: Session) -> File | None:
    archivo: File | None = db.get(File, id)

    return archivo
