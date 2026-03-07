from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.exceptions import IdYaUsadaException, NombreYaUsadoException
from app.models.folder import Folder
from app.models.user import User
from app.services.auth_services import get_current_user
from app.services.folder_services import crear_carpeta, obtener_carpetas_usuario
from app.schemas.folder_schemas import FolderBase, FolderRequest, FolderResponse

folder_router = APIRouter()


@folder_router.post("", response_model=FolderResponse)
def create_folder(req: FolderRequest, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        carpeta: Folder = crear_carpeta(
            nombre=req.nombre_carpeta, usuario=usuario, db=db)

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


@folder_router.get("", response_model=list[FolderBase])
def get_files(db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    carpetas: list[Folder] = obtener_carpetas_usuario(usuario=usuario, db=db)

    return [
        FolderBase(
            id=carpeta.id,
            nombre_original=carpeta.nombre_original,
            path=carpeta.path,
            fecha_creacion=carpeta.fecha_creacion,
            id_usuario=carpeta.id_usuario,
            nombre_usuario=carpeta.usuario.nombre
        )
        for carpeta in carpetas
    ]
