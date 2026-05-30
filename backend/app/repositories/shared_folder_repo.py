from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.carpeta_compartida import CarpetaCompartida
from app.models.carpeta_favorita import CarpetaFavorita
from app.models.folder import Folder


def add_shared_folder_db(carpeta_compartida: CarpetaCompartida, db: Session) -> CarpetaCompartida:
    db.add(carpeta_compartida)
    db.commit()
    db.refresh(carpeta_compartida)

    return carpeta_compartida


def get_shared_folder(id_carpeta: UUID, id_receptor: UUID, db: Session) -> CarpetaCompartida | None:
    return db.query(CarpetaCompartida).filter_by(id_carpeta=id_carpeta, id_receptor=id_receptor).first()


def get_shared_folder_no_receptor(id_compartido: UUID, id_propietario: UUID, db: Session) -> CarpetaCompartida | None:
    return db.query(CarpetaCompartida).filter_by(id=id_compartido, id_propietario=id_propietario).first()


def get_all_shared_folders_raiz(id_usuario: UUID, db: Session) -> list[CarpetaCompartida]:
    return (
        db.query(CarpetaCompartida)
        .options(
            joinedload(CarpetaCompartida.propietario),
            joinedload(CarpetaCompartida.receptor),
            joinedload(CarpetaCompartida.carpeta)
        )
        .filter_by(id_propietario=id_usuario).
        all()
    )


def get_all_received_folders_raiz(id_usuario: UUID, db: Session) -> list[CarpetaCompartida]:
    return (
        db.query(CarpetaCompartida)
        .options(
            joinedload(CarpetaCompartida.propietario),
            joinedload(CarpetaCompartida.receptor),
            joinedload(CarpetaCompartida.carpeta)
        )
        .filter_by(id_receptor=id_usuario).
        all()
    )


def get_all_shared_folders_raiz_paginadas(id_usuario: UUID, db: Session, offset: int, limit: int) -> tuple[int, list[CarpetaCompartida]]:
    query = (
        db.query(CarpetaCompartida)
        .options(
            joinedload(CarpetaCompartida.propietario),
            joinedload(CarpetaCompartida.receptor),
            joinedload(CarpetaCompartida.carpeta)
        )
        .filter_by(id_propietario=id_usuario)
    )

    total: int = query.count()

    carpetas_compartidas: list[CarpetaCompartida] = query.order_by(
        CarpetaCompartida.fecha_compartido.desc()).offset(offset).limit(limit).all()

    return total, carpetas_compartidas


def get_all_received_folders_raiz_paginadas(id_usuario: UUID, db: Session, offset: int, limit: int) -> tuple[int, list[CarpetaCompartida]]:
    query = (
        db.query(CarpetaCompartida)
        .options(
            joinedload(CarpetaCompartida.propietario),
            joinedload(CarpetaCompartida.receptor),
            joinedload(CarpetaCompartida.carpeta)
        )
        .filter_by(id_receptor=id_usuario)
    )

    total: int = query.count()

    carpetas_recibidas: list[CarpetaCompartida] = query.order_by(
        CarpetaCompartida.fecha_compartido.desc()).offset(offset).limit(limit).all()

    return total, carpetas_recibidas


def get_all_shared_folders_raiz_sorted(id_usuario: UUID, db: Session, busqueda: str | None = None) -> list[tuple[CarpetaCompartida, bool]]:
    exists_favorito = db.query(CarpetaFavorita.id).filter(
        CarpetaFavorita.id_carpeta == CarpetaCompartida.id_carpeta,
        CarpetaFavorita.id_usuario == id_usuario
    ).exists()

    query = (
        db.query(CarpetaCompartida, exists_favorito.label("favorito"))
        .options(
            joinedload(CarpetaCompartida.propietario),
            joinedload(CarpetaCompartida.receptor),
            joinedload(CarpetaCompartida.carpeta)
        )
        .filter_by(id_propietario=id_usuario)
    )

    if busqueda:
        query = query.join(CarpetaCompartida.carpeta).filter(
            Folder.nombre_original.ilike(f"%{busqueda}%")
        )

    return query.order_by(CarpetaCompartida.fecha_compartido.desc()).all()


def get_all_received_folders_raiz_sorted(id_usuario: UUID, db: Session, busqueda: str | None = None) -> list[tuple[CarpetaCompartida, bool]]:
    exists_favorito = db.query(CarpetaFavorita.id).filter(
        CarpetaFavorita.id_carpeta == CarpetaCompartida.id_carpeta,
        CarpetaFavorita.id_usuario == id_usuario
    ).exists()

    query = (
        db.query(CarpetaCompartida, exists_favorito.label("favorito"))
        .options(
            joinedload(CarpetaCompartida.propietario),
            joinedload(CarpetaCompartida.receptor),
            joinedload(CarpetaCompartida.carpeta)
        )
        .filter_by(id_receptor=id_usuario)
    )

    if busqueda:
        query = query.join(CarpetaCompartida.carpeta).filter(
            Folder.nombre_original.ilike(f"%{busqueda}%")
        )

    return query.order_by(CarpetaCompartida.fecha_compartido.desc()).all()
