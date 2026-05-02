from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse as FileResp
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.middleware.pagination_middleware import get_pagination
from app.models.user import User
from app.models import exceptions as ex
from app.schemas import file_schemas
from app.middleware.auth_middleware import get_current_user
from app.services import file_services

file_router = APIRouter()


@file_router.get("", response_model=file_schemas.PaginatedFileResponse)
def get_files(db: Session = Depends(get_db), usuario: User = Depends(get_current_user), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, archivos = file_services.obtener_archivos_usuario_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": [
            file_schemas.FileBase(
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
        ],
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@file_router.post("", response_model=file_schemas.FileResponse)
async def upload_file(file_upload: list[UploadFile] = File(...), db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivos: list[File] = []
        for file in file_upload:
            archivo_db: File = await file_services.guardar_archivo(file_upload=file, db=db, usuario=usuario)
            archivos.append(archivo_db)

        return {
            "msg": "Archivos guardados con éxito",
            "archivos": [
                file_schemas.FileBase(
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
    except ex.TamañoExcedidoException as e1:
        raise HTTPException(413, str(e1))
    except ex.IdYaUsadaException as e2:
        raise HTTPException(409, str(e2))
    except ex.NombreYaUsadoException as e3:
        raise HTTPException(409, str(e3))


@file_router.get("/trash", response_model=file_schemas.PaginatedFileResponse)
def get_files_trash(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, archivos = file_services.obtener_archivos_papelera_raiz_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": [
            file_schemas.FileBase(
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
        ],
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@file_router.delete("/trash/{id_archivo}", response_model=file_schemas.DeleteFilePermanentResponse)
def delete_file_permanent(id_archivo: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        file_services.eliminar_archivo_permanente(
            id_archivo=id_archivo, db=db, usuario=usuario)

        return {
            "msg": "Archivo eliminado correctamente"
        }
    except ex.ArchivoNoEncontradoException:
        raise HTTPException(
            404, detail="No se ha encontrado el archivo en la papelera")
    except ex.EliminarDiscoException as e2:
        raise HTTPException(500, detail=str(e2))


@file_router.get("/{id_archivo}", response_class=FileResp)
def download_files(id_archivo: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivo: File = file_services.obtener_archivo_permisos(
            id_archivo=id_archivo, usuario=usuario, db=db)

        return FileResp(path=archivo.path, filename=archivo.nombre_original)
    except ex.ArchivoNoEncontradoException:
        raise HTTPException(
            404, detail=f"No se ha encontrado el archivo con id {id_archivo}")


@file_router.put("/{id_archivo}/restaurar", response_model=file_schemas.RestoreFileResponse)
def restore_file_from_trash(id_archivo: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivo: File = file_services.restaurar_archivo_papelera(
            id_archivo=id_archivo, db=db, usuario=usuario)

        return {
            "msg": "Archivo restaurado correctamente",
            "archivo": file_schemas.FileBase(
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

    except ex.ArchivoNoEncontradoException:
        raise HTTPException(
            404, detail=f"No se ha encontrado el archivo con ID {id_archivo} en la papelera")


@file_router.delete("/{id_archivo}", response_model=file_schemas.AddFileTrashResponse)
def add_file_to_trash(id_archivo: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivo: File = file_services.añadir_archivo_papelera(
            id_archivo=id_archivo, db=db, usuario=usuario)

        return {
            "msg": "Archivo enviado a la papelera con éxito",
            "archivo": file_schemas.FileBase(
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

    except ex.ArchivoNoEncontradoException:
        raise HTTPException(
            404, detail=f"No se ha encontrado el archivo con ID {id_archivo}")
    except ex.ArchivoPapeleraException:
        raise HTTPException(
            409, detail="El archivo seleccionado ya está en la papelera")
