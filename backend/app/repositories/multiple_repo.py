from sqlalchemy.orm import Session

from app.models.file import File
from app.models.folder import Folder


# Sin commit porque esperamos a que se recorra toda la lista
def delete_file(archivo: File, db: Session):
    db.delete(archivo)


def delete_folder(carpeta: Folder, db: Session):
    db.delete(carpeta)
