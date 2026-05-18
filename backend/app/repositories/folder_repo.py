import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session, aliased

from app.models.carpeta_compartida import CarpetaCompartida
from app.models.folder import Folder
from app.models.user import User


def add_folder(carpeta: Folder, db: Session) -> Folder:
    db.add(carpeta)
    db.commit()
    db.refresh(carpeta)

    return carpeta


def update_folder(carpeta: Folder, db: Session) -> Folder:
    db.commit()
    db.refresh(carpeta)

    return carpeta


def get_folder_id_user(id: uuid.UUID, usuario: User, db: Session) -> Folder | None:
    return db.query(Folder).filter(Folder.id == id, Folder.id_usuario == usuario.id, Folder.fecha_eliminacion == None).first()


def get_folder_original_name(nombre_original: str, usuario: User, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(nombre_original=nombre_original, id_usuario=usuario.id).first()


def get_folders_user(id_usuario: uuid.UUID, db: Session) -> list[Folder]:
    return db.query(Folder).filter_by(id_usuario=id_usuario).all()


def get_folder_name_anidada(id_carpeta_padre: str, nombre_carpeta: str, usuario: User, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(id_usuario=usuario.id, nombre_original=nombre_carpeta, id_carpeta=id_carpeta_padre).first()


def get_folder_id(id_carpeta: str, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(id=id_carpeta).first()


def get_folders_user_raiz(id_usuario: uuid.UUID, db: Session) -> list[Folder]:
    return db.query(Folder).filter(Folder.id_usuario == id_usuario, Folder.id_carpeta == None, Folder.fecha_eliminacion == None).all()


def get_folder_nombre_raiz(nombre_carpeta: str, id_usuario: uuid.UUID, db: Session) -> Folder | None:
    return db.query(Folder).filter_by(nombre_original=nombre_carpeta, id_usuario=id_usuario, id_carpeta=None).first()


def get_folders_inside_folder(id_carpeta: uuid.UUID, id_usuario: uuid.UUID, db: Session) -> list[Folder]:
    return db.query(Folder).filter_by(id_carpeta=id_carpeta, id_usuario=id_usuario).all()


def get_folder_trash(id_carpeta: uuid.UUID, id_usuario: uuid.UUID, db: Session) -> Folder | None:
    return db.query(Folder).filter(Folder.id == id_carpeta, Folder.id_usuario == id_usuario, Folder.fecha_eliminacion != None).first()


def get_all_folders_trash_raiz(id_usuario: uuid.UUID, db: Session) -> list[Folder]:
    # Obtener carpetas que están eliminadas y están en la raíz o las que están eliminadas pero su carpeta no lo está
    CarpetaPadre = aliased(Folder)

    query = db.query(Folder).outerjoin(
        CarpetaPadre, Folder.id_carpeta == CarpetaPadre.id
    ).filter(
        Folder.id_usuario == id_usuario,
        Folder.fecha_eliminacion != None,
        or_(
            Folder.id_carpeta == None,
            CarpetaPadre.fecha_eliminacion == None
        )
    )

    return query.order_by(Folder.fecha_eliminacion.desc()).all()


def delete_folder(carpeta: Folder, db: Session):
    db.delete(carpeta)
    db.commit()


def get_folders_user_raiz_paginadas(id_usuario: uuid.UUID, db: Session, offset: int, limit: int) -> tuple[int, list[Folder]]:
    query = db.query(Folder).filter(Folder.id_usuario == id_usuario,
                                    Folder.id_carpeta == None, Folder.fecha_eliminacion == None)

    total: int = query.count()

    carpetas: list[Folder] = query.order_by(
        Folder.fecha_creacion.desc()).offset(offset).limit(limit).all()

    return total, carpetas


def get_all_folders_trash_raiz_paginadas(id_usuario: uuid.UUID, db: Session, offset: int, limit: int) -> tuple[int, list[Folder]]:
   # Obtener carpetas que están eliminadas y están en la raíz o las que están eliminadas pero su carpeta no lo está
    CarpetaPadre = aliased(Folder)

    query = db.query(Folder).outerjoin(
        CarpetaPadre, Folder.id_carpeta == CarpetaPadre.id
    ).filter(
        Folder.id_usuario == id_usuario,
        Folder.fecha_eliminacion != None,
        or_(
            Folder.id_carpeta == None,
            CarpetaPadre.fecha_eliminacion == None
        )
    )

    total: int = query.count()

    carpetas: list[Folder] = query.order_by(
        Folder.fecha_eliminacion.desc()).offset(offset).limit(limit).all()

    return total, carpetas


def get_folders_inside_folder_paginadas(id_carpeta: uuid.UUID, id_usuario: uuid.UUID, db: Session, offset: int, limit: int) -> tuple[int, list[Folder]]:
    query = (
        db.query(Folder)
        .outerjoin(CarpetaCompartida, CarpetaCompartida.id_carpeta == Folder.id)
        .filter(
            Folder.id_carpeta == id_carpeta,
            or_(
                Folder.id_usuario == id_usuario,
                CarpetaCompartida.id_receptor == id_usuario,
                Folder.id_carpeta.in_(
                    db.query(CarpetaCompartida.id_carpeta).filter(
                        CarpetaCompartida.id_receptor == id_usuario)
                )
            )
        )
    )

    total: int = query.count()

    carpetas: list[Folder] = query.order_by(
        Folder.fecha_creacion.desc()).offset(offset).limit(limit).all()

    return total, carpetas


def get_folders_user_raiz_sorted(id_usuario: uuid.UUID, db: Session, busqueda: str | None = None) -> list[Folder]:
    query = db.query(Folder).filter(
        Folder.id_usuario == id_usuario,
        Folder.id_carpeta == None,
        Folder.fecha_eliminacion == None
    )

    if busqueda:
        query = query.filter(Folder.nombre_original.ilike(f"%{busqueda}%"))

    return query.order_by(Folder.fecha_creacion.desc()).all()


# O propietario o usuario con permisos (acordarme de cambiarlo en algún momento en el resto de queries antiguas)
def get_folders_inside_folder_sorted(id_carpeta: uuid.UUID, id_usuario: uuid.UUID, db: Session, busqueda: str | None = None) -> list[Folder]:
    query = (
        db.query(Folder)
        .outerjoin(CarpetaCompartida, CarpetaCompartida.id_carpeta == Folder.id)
        .filter(
            Folder.id_carpeta == id_carpeta,
            Folder.fecha_eliminacion == None,
            or_(
                Folder.id_usuario == id_usuario,
                CarpetaCompartida.id_receptor == id_usuario,
                Folder.id_carpeta.in_(
                    db.query(CarpetaCompartida.id_carpeta).filter(
                        CarpetaCompartida.id_receptor == id_usuario
                    )
                )
            )
        )
    )

    if busqueda:
        query = query.filter(Folder.nombre_original.ilike(f"%{busqueda}%"))

    return query.order_by(Folder.fecha_creacion.desc()).all()


def get_all_folders_trash_raiz_sorted(id_usuario: uuid.UUID, db: Session, busqueda: str | None = None) -> list[Folder]:
    # Obtener carpetas que están eliminadas y están en la raíz o las que están eliminadas pero su carpeta no lo está
    CarpetaPadre = aliased(Folder)

    query = db.query(Folder).outerjoin(
        CarpetaPadre, Folder.id_carpeta == CarpetaPadre.id
    ).filter(
        Folder.id_usuario == id_usuario,
        Folder.fecha_eliminacion != None,
        or_(
            Folder.id_carpeta == None,
            CarpetaPadre.fecha_eliminacion == None
        )
    )

    if busqueda:
        query = query.filter(Folder.nombre_original.ilike(f"%{busqueda}%"))

    return query.order_by(Folder.fecha_eliminacion.desc()).all()
