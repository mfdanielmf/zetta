import os
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.file import File
from app.models.user import User
from app.models import exceptions as ex
from app.services import file_services
from app.repositories import file_repo


def eliminar_multiples_archivos_permanente(ids: list[UUID], usuario: User, db: Session):
    """
    ArchivoNoEncontradoException, EliminarDiscoException
    """
    errores = []

    for id_archivo in ids:
        nombre_archivo = "desconocido"

        try:
            archivo: File = file_services.obtener_archivo_papelera(
                id_archivo=id_archivo,
                usuario=usuario,
                db=db
            )

            nombre_archivo = archivo.nombre_original or "desconocido"

            path: str = archivo.path

            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    raise ex.EliminarDiscoException(
                        "Error al eliminar el archivo del disco"
                    )

            file_repo.delete_file(archivo=archivo, db=db)

        except Exception as e1:
            errores.append({
                "id_archivo": str(id_archivo),
                "nombre_archivo": nombre_archivo,
                "error": str(e1)
            })

    db.commit()

    return errores
