from sqlalchemy.orm import Session

from app.models.folder import Folder

def add_folder(carpeta: Folder, db: Session) -> Folder:
    db.add(carpeta)
    db.commit()
    db.flush(carpeta)

    return carpeta