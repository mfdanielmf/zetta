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
