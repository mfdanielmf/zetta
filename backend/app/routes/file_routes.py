from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse as FileResp
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.models.user import User
from app.services.file_services import guardar_archivo, obtener_archivos_usuario, obtener_archivo_id, añadir_archivo_papelera
from app.models.exceptions import ArchivoNoEncontradoException, TamañoExcedidoException, IdYaUsadaException, NombreYaUsadoException
from app.schemas.file_schemas import AddTrashResponse, FileBase, FileResponse
from app.services.auth_services import get_current_user

file_router = APIRouter()


@file_router.get("", response_model=list[FileBase])
def get_files(db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    archivos: list[File] = obtener_archivos_usuario(usuario=usuario, db=db)

    return [
        FileBase(
            id=archivo_db.id,
            nombre_original=archivo_db.nombre_original,
            path=archivo_db.path,
            tamaño_bytes=archivo_db.tamaño_bytes,
            fecha_creacion=archivo_db.fecha_creacion,
            id_usuario=archivo_db.id_usuario,
            nombre_usuario=archivo_db.usuario.nombre,
            id_carpeta=archivo_db.id_carpeta,
            fecha_eliminacion=archivo_db.fecha_eliminacion
        )
        for archivo_db in archivos
    ]


@file_router.post("", response_model=FileResponse)
async def upload_file(file_upload: list[UploadFile] = File(...), db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivos: list[File] = []
        for file in file_upload:
            archivo_db: File = await guardar_archivo(file_upload=file, db=db, usuario=usuario)
            archivos.append(archivo_db)

        return {
            "msg": "Archivos guardados con éxito",
            "archivos": [
                FileBase(
                    id=archivo.id,
                    nombre_original=archivo.nombre_original,
                    path=archivo.path,
                    tamaño_bytes=archivo.tamaño_bytes,
                    fecha_creacion=archivo.fecha_creacion,
                    id_usuario=archivo.id_usuario,
                    nombre_usuario=archivo.usuario.nombre,
                    id_carpeta=archivo.id_carpeta,
                    fecha_eliminacion=archivo.fecha_eliminacion
                ) for archivo in archivos
            ]
        }
    except TamañoExcedidoException as e1:
        raise HTTPException(413, str(e1))
    except IdYaUsadaException as e2:
        raise HTTPException(409, str(e2))
    except NombreYaUsadoException as e3:
        raise HTTPException(409, str(e3))


@file_router.get("/{id_archivo}", response_class=FileResp)
def download_files(id_archivo: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivo: File = obtener_archivo_id(
            id=id_archivo, usuario=usuario, db=db)

        return FileResp(path=archivo.path, filename=archivo.nombre_original)
    except ArchivoNoEncontradoException:
        raise HTTPException(
            404, detail=f"No se ha encontrado el archivo con id {id_archivo}")


@file_router.delete("/{id_archivo}", response_model=AddTrashResponse)
def add_file_to_trash(id_archivo: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivo: File = añadir_archivo_papelera(
            id_archivo=id_archivo, db=db, usuario=usuario)

        return {
            "msg": "Archivo enviado a la papelera con éxito",
            "archivo": FileBase(
                id=archivo.id,
                nombre_original=archivo.nombre_original,
                path=archivo.path,
                tamaño_bytes=archivo.tamaño_bytes,
                fecha_creacion=archivo.fecha_creacion,
                id_usuario=archivo.id_usuario,
                nombre_usuario=archivo.usuario.nombre,
                id_carpeta=archivo.id_carpeta,
                fecha_eliminacion=archivo.fecha_eliminacion
            )
        }

    except ArchivoNoEncontradoException:
        raise HTTPException(
            404, detail=f"No se ha encontrado el archivo con ID {id_archivo}")
