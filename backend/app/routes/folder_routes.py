from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FileFA
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.exceptions import IdYaUsadaException, NombreYaUsadoException, TamañoExcedidoException, CarpetaNoEncontradaException
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.schemas.file_schemas import FileBase
from app.services.auth_services import get_current_user
from app.services.folder_services import crear_carpeta, obtener_carpetas_usuario, guardar_archivo_carpeta
from app.schemas.folder_schemas import FolderBase, FolderRequest, FolderResponse, UploadFileFolderResponse

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


@folder_router.post("/{id_carpeta}/files", response_model=UploadFileFolderResponse)
async def upload_file_to_folder(id_carpeta: UUID, archivo: UploadFile = FileFA(...), db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivo_guardado: File = await guardar_archivo_carpeta(
            id_carpeta=id_carpeta, file_upload=archivo, db=db, usuario=usuario)

        return {
            "msg": "Archivo subido correctamente",
            "archivo": FileBase(
                id=archivo_guardado.id,
                nombre_original=archivo_guardado.nombre_original,
                path=archivo_guardado.path,
                tamaño_bytes=archivo_guardado.tamaño_bytes,
                fecha_creacion=archivo_guardado.fecha_creacion,
                id_usuario=archivo_guardado.id_usuario,
                nombre_usuario=archivo_guardado.usuario.nombre,
                id_carpeta=archivo_guardado.id_carpeta
            )
        }
    except TamañoExcedidoException as e1:
        raise HTTPException(413, str(e1))
    except CarpetaNoEncontradaException as e2:
        raise HTTPException(404, str(e2))
