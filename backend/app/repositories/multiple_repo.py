from sqlalchemy.orm import Session

from app.models.file import File


# Sin commit porque esperamos a que se recorra toda la lista
def delete_file(archivo: File, db: Session):
    db.delete(archivo)
