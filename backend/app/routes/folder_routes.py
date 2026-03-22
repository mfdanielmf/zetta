from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FileFA
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.exceptions import IdYaUsadaException, NombreYaUsadoException, TamañoExcedidoException, CarpetaNoEncontradaException
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.schemas.file_schemas import FileBase
from app.services.file_services import obtener_archivos_carpeta
from app.services.auth_services import get_current_user
from app.services.folder_services import crear_carpeta, obtener_carpetas_usuario, guardar_archivo_carpeta, crear_carpeta_anidada
from app.schemas.folder_schemas import FolderBase, FolderRequest, FolderResponse, UploadFileFolderResponse

folder_router = APIRouter()


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


@folder_router.get("/{id_carpeta}/files", response_model=list[FileBase])
def get_files_of_folder(id_carpeta: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivos: list[File] = obtener_archivos_carpeta(
            db=db, id_carpeta=id_carpeta, usuario=usuario)
    except CarpetaNoEncontradaException:
        raise HTTPException(
            404, f"No se ha encontrado la carpeta con id {id_carpeta}")

    return [
        FileBase(
            id=archivo.id,
            nombre_original=archivo.nombre_original,
            path=archivo.path,
            tamaño_bytes=archivo.tamaño_bytes,
            fecha_creacion=archivo.fecha_creacion,
            id_usuario=archivo.id_usuario,
            nombre_usuario=archivo.usuario.nombre,
            id_carpeta=archivo.id_carpeta
        )
        for archivo in archivos
    ]


@folder_router.post("/{id_carpeta}/files", response_model=UploadFileFolderResponse)
async def upload_file_to_folder(id_carpeta: UUID, file_upload: list[UploadFile] = FileFA(...), db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivos: list[File] = []
        for file in file_upload:
            archivo_db: File = await guardar_archivo_carpeta(id_carpeta=id_carpeta, file_upload=file, db=db, usuario=usuario)
            archivos.append(archivo_db)

        return {
            "msg": "Archivos subidos correctamente",
            "archivos": [
                FileBase(
                    id=archivo_guardado.id,
                    nombre_original=archivo_guardado.nombre_original,
                    path=archivo_guardado.path,
                    tamaño_bytes=archivo_guardado.tamaño_bytes,
                    fecha_creacion=archivo_guardado.fecha_creacion,
                    id_usuario=archivo_guardado.id_usuario,
                    nombre_usuario=archivo_guardado.usuario.nombre,
                    id_carpeta=archivo_guardado.id_carpeta
                )
                for archivo_guardado in archivos
            ]
        }
    except TamañoExcedidoException as e1:
        raise HTTPException(413, str(e1))
    except CarpetaNoEncontradaException as e2:
        raise HTTPException(404, str(e2))
    except NombreYaUsadoException as e3:
        raise HTTPException(409, str(e3))


@folder_router.post("/{id_carpeta}/folders", response_model=FolderResponse)
def upload_file_to_folder(id_carpeta: UUID, req: FolderRequest, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        carpeta: Folder = crear_carpeta_anidada(
            id_carpeta_padre=id_carpeta, nombre=req.nombre_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta creada correctamente",
            "carpeta": FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                id_carpeta=id_carpeta
            )
        }
    except IdYaUsadaException as e:
        raise HTTPException(409, str(e))
    except NombreYaUsadoException as e2:
        raise HTTPException(409, str(e2))
    except CarpetaNoEncontradaException as e3:
        raise HTTPException(404, str(e3))
