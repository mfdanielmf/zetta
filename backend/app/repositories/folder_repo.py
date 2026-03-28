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


def get_folders_user(id_usuario: uuid.UUID, db: Session) -> list[Folder]:
    return db.query(Folder).filter_by(id_usuario=id_usuario).all()


def get_folder_name_anidada(id_carpeta_padre: str, nombre_carpeta: str, usuario: User, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(id_usuario=usuario.id, nombre_original=nombre_carpeta, id_carpeta=id_carpeta_padre).first()


def get_folder_id(id_carpeta: str, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(id=id_carpeta).first()


def get_folders_user_raiz(id_usuario: uuid.UUID, db: Session) -> list[Folder]:
    return db.query(Folder).filter_by(id_usuario=id_usuario, id_carpeta=None).all()


def get_folder_nombre_raiz(nombre_carpeta: str, id_usuario: uuid.UUID, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(nombre_original=nombre_carpeta, id_usuario=id_usuario, id_carpeta=None).first()


def get_folders_inside_folder(id_carpeta: uuid.UUID, id_usuario: uuid.UUID, db: Session) -> list[Folder]:
    return db.query(Folder).filter_by(id_carpeta=id_carpeta, id_usuario=id_usuario).all()
