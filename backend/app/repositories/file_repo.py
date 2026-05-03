import uuid
from app.models.file import File
from sqlalchemy.orm import Session

from app.models.user import User


def insert_file_db(archivo: File, db: Session) -> File:
    db.add(archivo)
    db.commit()
    db.refresh(archivo)

    return archivo


def update_file(archivo: File, db: Session) -> File:
    db.commit()
    db.refresh(archivo)

    return archivo


def get_file_by_id(id_archivo: uuid.UUID, db: Session) -> File | None:
    return db.query(File).filter_by(id=id_archivo).first()


def get_file_by_id_and_user(id: uuid.UUID, usuario: User, db: Session) -> File | None:
    return db.query(File).filter(File.id == id, File.id_usuario == usuario.id, File.fecha_eliminacion == None).first()


def get_files_user(usuario: User, db: Session) -> list[File]:
    return db.query(File).filter_by(id_usuario=usuario.id).all()


def get_file_original_name(nombre_original: str, usuario: User, db: Session) -> File | None:
    return db.query(File).filter_by(nombre_original=nombre_original, id_usuario=usuario.id).first()


def get_file_by_name_in_folder(nombre_original: str, usuario: User, db: Session, id_carpeta: uuid.UUID | None = None) -> File | None:
    return db.query(File).filter_by(nombre_original=nombre_original, id_carpeta=id_carpeta, id_usuario=usuario.id).first()


def get_all_files_in_folder(id_carpeta: uuid.UUID, db: Session, usuario: User) -> list[File]:
    return db.query(File).filter_by(id_carpeta=id_carpeta, id_usuario=usuario.id).all()


def get_file_trash(id_archivo: uuid.UUID, id_usuario: uuid.UUID, db: Session) -> File | None:
    return db.query(File).filter(File.id == id_archivo, File.id_usuario == id_usuario, File.fecha_eliminacion != None).first()


def get_all_files_trash_raiz(id_usuario: uuid.UUID, db: Session) -> list[File]:
    return db.query(File).filter(File.id_usuario == id_usuario, File.fecha_eliminacion != None, File.id_carpeta == None).all()


def get_files_raiz(id_usuario: uuid.UUID, db: Session) -> list[File]:
    return db.query(File).filter(File.id_usuario == id_usuario, File.id_carpeta == None, File.fecha_eliminacion == None).all()


def delete_file(archivo: File, db: Session):
    db.delete(archivo)
    db.commit()


def get_files_raiz_paginados(id_usuario: uuid.UUID, db: Session, offset: int, limit: int) -> tuple[int, list[File]]:
    query = db.query(File).filter(File.id_usuario == id_usuario,
                                  File.id_carpeta == None, File.fecha_eliminacion == None)

    total: int = query.count()

    archivos: list[File] = query.order_by(
        File.fecha_creacion.desc()).offset(offset).limit(limit).all()

    return total, archivos


def get_all_files_trash_raiz_paginados(id_usuario: uuid.UUID, db: Session, offset: int, limit: int) -> tuple[int, list[File]]:
    query = db.query(File).filter(File.id_usuario == id_usuario,
                                  File.fecha_eliminacion != None, File.id_carpeta == None)

    total: int = query.count()

    archivos: list[File] = query.order_by(
        File.fecha_creacion.desc()).offset(offset).limit(limit).all()

    return total, archivos


def get_all_files_in_folder_paginados(id_carpeta: uuid.UUID, db: Session, id_usuario: uuid.UUID, offset: int, limit: int) -> tuple[int, list[File]]:
    query = db.query(File).filter(File.id_carpeta ==
                                  id_carpeta, File.id_usuario == id_usuario)

    total: int = query.count()

    archivos: list[File] = query.order_by(
        File.fecha_creacion.desc()).offset(offset).limit(limit).all()

    return total, archivos


def get_files_raiz_sorted(id_usuario: uuid.UUID, db: Session) -> list[File]:
    return db.query(File).filter(File.id_usuario == id_usuario, File.id_carpeta == None, File.fecha_eliminacion == None).order_by(File.fecha_creacion.desc()).all()


def get_all_files_in_folder_sorted(id_carpeta: uuid.UUID, db: Session, id_usuario: uuid.UUID) -> list[File]:
    return db.query(File).filter_by(id_carpeta=id_carpeta, id_usuario=id_usuario).order_by(File.fecha_creacion.desc()).all()
