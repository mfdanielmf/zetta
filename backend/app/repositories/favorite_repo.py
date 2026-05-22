from sqlalchemy import UUID
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.folder import Folder


def get_favorite_folders(id_usuario: UUID, db: Session, busqueda: str | None = None) -> list[Folder]:
    query = db.query(Folder).filter(
        Folder.id_usuario == id_usuario,
        Folder.fecha_eliminacion == None,
        Folder.favorito == True
    )

    if busqueda:
        query.filter(Folder.nombre_original.ilike(f"%{busqueda}%"))

    return query.order_by(Folder.fecha_favorito.desc()).all()


def get_favorite_files(id_usuario: UUID, db: Session, busqueda: str | None = None) -> list[File]:
    query = db.query(File).filter(
        File.id_usuario == id_usuario,
        File.fecha_eliminacion == None,
        File.favorito == True
    )

    if busqueda:
        query.filter(File.nombre_original.ilike(f"%{busqueda}%"))

    return query.order_by(File.fecha_favorito.desc()).all()
