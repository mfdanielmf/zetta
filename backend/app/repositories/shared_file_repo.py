from uuid import UUID

from sqlalchemy.orm import Session

from app.models.archivo_compartido import ArchivoCompartido


def add_shared_file_db(archivo_compartido: ArchivoCompartido, db: Session) -> ArchivoCompartido:
    db.add(archivo_compartido)
    db.commit()
    db.refresh(archivo_compartido)

    return archivo_compartido


def get_shared_file(id_archivo: UUID, id_receptor: UUID, db: Session) -> ArchivoCompartido:
    return db.query(ArchivoCompartido).filter_by(id_archivo=id_archivo, id_receptor=id_receptor).first()
