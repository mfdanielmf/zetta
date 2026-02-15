from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.models.user import User
from app.services.file_services import guardar_archivo, obtener_archivos_usuario
from app.models.exceptions import TamañoExcedidoException, IdYaUsadaException
from app.schemas.file_schemas import FileBase, FileResponse
from app.services.auth_services import get_current_user

file_router = APIRouter()


@file_router.post("", response_model=FileResponse)
async def upload_file(file_upload: UploadFile = File(...), db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivo_db: File = await guardar_archivo(file_upload=file_upload, db=db, usuario=usuario)

        return {
            "msg": "Archivo guardado con éxito",
            "archivo": FileBase(
                id=archivo_db.id,
                nombre_original=archivo_db.nombre_original,
                path=archivo_db.path,
                tamaño_bytes=archivo_db.tamaño_bytes,
                fecha_creacion=archivo_db.fecha_creacion,
                id_usuario=archivo_db.id_usuario,
                nombre_usuario=archivo_db.usuario.nombre
            )
        }
    except TamañoExcedidoException as e1:
        raise HTTPException(413, str(e1))
    except IdYaUsadaException as e2:
        raise HTTPException(409, str(e2))


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
            nombre_usuario=archivo_db.usuario.nombre
        )
        for archivo_db in archivos
    ]
