from sqlalchemy import UUID
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.folder import Folder
from app.models.carpeta_favorita import CarpetaFavorita
from app.models.archivo_favorito import ArchivoFavorito


def get_favorite_folders(id_usuario: UUID, db: Session, busqueda: str | None = None) -> list[CarpetaFavorita]:
    query = db.query(CarpetaFavorita).join(Folder).filter(
        CarpetaFavorita.id_usuario == id_usuario,
        Folder.fecha_eliminacion == None
    )

    if busqueda:
        query = query.filter(
            Folder.nombre_original.ilike(f"%{busqueda}%"))

    return query.order_by(CarpetaFavorita.fecha_favorito.desc()).all()


def get_favorite_files(id_usuario: UUID, db: Session, busqueda: str | None = None) -> list[ArchivoFavorito]:
    query = db.query(ArchivoFavorito).join(File).filter(
        ArchivoFavorito.id_usuario == id_usuario,
        File.fecha_eliminacion == None
    )

    if busqueda:
        query = query.filter(
            File.nombre_original.ilike(f"%{busqueda}%"))

    return query.order_by(ArchivoFavorito.fecha_favorito.desc()).all()


def get_favorite_folder_user_by_folder_id(id_carpeta: UUID, id_usuario: UUID, db: Session) -> CarpetaFavorita | None:
    return db.query(CarpetaFavorita).filter_by(id_carpeta=id_carpeta, id_usuario=id_usuario).first()


def get_favorite_file_user_by_file_id(id_archivo: UUID, id_usuario: UUID, db: Session) -> ArchivoFavorito | None:
    return db.query(ArchivoFavorito).filter_by(id_archivo=id_archivo, id_usuario=id_usuario).first()


def delete_favorite_file_no_commit(favorito: ArchivoFavorito, db: Session):
    db.delete(favorito)


def delete_favorite_folder_no_commit(favorito: CarpetaFavorita, db: Session):
    db.delete(favorito)


def add_favorite_file_no_commit(favorito: ArchivoFavorito, db: Session) -> ArchivoFavorito:
    db.add(favorito)
    db.flush()
    db.refresh(favorito)

    return favorito


def add_favorite_folder_no_commit(favorito: ArchivoFavorito, db: Session) -> ArchivoFavorito:
    db.add(favorito)
    db.flush()
    db.refresh(favorito)

    return favorito
