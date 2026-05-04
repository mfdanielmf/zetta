from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.archivo_compartido import ArchivoCompartido


def add_shared_file_db(archivo_compartido: ArchivoCompartido, db: Session) -> ArchivoCompartido:
    db.add(archivo_compartido)
    db.commit()
    db.refresh(archivo_compartido)

    return archivo_compartido


def get_shared_file(id_archivo: UUID, id_receptor: UUID, db: Session) -> ArchivoCompartido | None:
    return db.query(ArchivoCompartido).filter_by(id_archivo=id_archivo, id_receptor=id_receptor).first()


def get_all_shared_files_raiz(id_usuario: UUID, db: Session) -> list[ArchivoCompartido]:
    return (
        db.query(ArchivoCompartido)
        .options(
            joinedload(ArchivoCompartido.propietario),
            joinedload(ArchivoCompartido.receptor),
            joinedload(ArchivoCompartido.archivo)
        )
        .filter_by(id_propietario=id_usuario).
        all()
    )


def get_all_received_files_raiz(id_usuario: UUID, db: Session) -> list[ArchivoCompartido]:
    return (
        db.query(ArchivoCompartido)
        .options(
            joinedload(ArchivoCompartido.propietario),
            joinedload(ArchivoCompartido.receptor),
            joinedload(ArchivoCompartido.archivo)
        )
        .filter_by(id_receptor=id_usuario).all()
    )


def get_all_shared_files_raiz_paginados(id_usuario: UUID, db: Session, offset: int, limit: int) -> tuple[int, list[ArchivoCompartido]]:
    query = (
        db.query(ArchivoCompartido)
        .options(
            joinedload(ArchivoCompartido.propietario),
            joinedload(ArchivoCompartido.receptor),
            joinedload(ArchivoCompartido.archivo)
        )
        .filter_by(id_propietario=id_usuario)
    )

    total: int = query.count()

    archivos_compartidos: list[ArchivoCompartido] = query.order_by(
        ArchivoCompartido.fecha_compartido.desc()).offset(offset).limit(limit).all()

    return total, archivos_compartidos


def get_all_received_files_raiz_paginados(id_usuario: UUID, db: Session, offset: int, limit: int) -> tuple[int, list[ArchivoCompartido]]:
    query = (
        db.query(ArchivoCompartido)
        .options(
            joinedload(ArchivoCompartido.propietario),
            joinedload(ArchivoCompartido.receptor),
            joinedload(ArchivoCompartido.archivo)
        )
        .filter_by(id_receptor=id_usuario)
    )

    total: int = query.count()

    archivos_recibidos: list[ArchivoCompartido] = query.order_by(
        ArchivoCompartido.fecha_compartido.desc()).offset(offset).limit(limit).all()

    return total, archivos_recibidos


def get_all_shared_files_raiz_sorted(id_usuario: UUID, db: Session) -> list[ArchivoCompartido]:
    return (
        db.query(ArchivoCompartido)
        .options(
            joinedload(ArchivoCompartido.propietario),
            joinedload(ArchivoCompartido.receptor),
            joinedload(ArchivoCompartido.archivo)
        )
        .filter_by(id_propietario=id_usuario)
        .order_by(ArchivoCompartido.fecha_compartido.desc())
        .all()
    )
