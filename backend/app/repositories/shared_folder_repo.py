from uuid import UUID

from sqlalchemy.orm import Session

from app.models.carpeta_compartida import CarpetaCompartida


def add_shared_folder_db(carpeta_compartida: CarpetaCompartida, db: Session) -> CarpetaCompartida:
    db.add(carpeta_compartida)
    db.commit()
    db.refresh(carpeta_compartida)

    return carpeta_compartida


def get_shared_folder(id_carpeta: UUID, id_receptor: UUID, db: Session) -> CarpetaCompartida | None:
    return db.query(CarpetaCompartida).filter_by(id_carpeta=id_carpeta, id_receptor=id_receptor).first()
