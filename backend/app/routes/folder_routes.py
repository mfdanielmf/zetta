from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.exceptions import IdYaUsadaException, NombreYaUsadoException
from app.models.folder import Folder
from app.models.user import User
from app.services.auth_services import get_current_user
from app.services.folder_services import crear_carpeta
from app.schemas.folder_schemas import FolderBase, FolderResponse

folder_router = APIRouter()


@folder_router.post("", response_model=FolderResponse)
def create_folder(nombre_carpeta: str, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        carpeta: Folder = crear_carpeta(
            nombre=nombre_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta creada correctamente",
            "carpeta": FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre
            )
        }
    except IdYaUsadaException as e:
        raise HTTPException(409, str(e))
    except NombreYaUsadoException as e2:
        raise HTTPException(409, str(e2))
