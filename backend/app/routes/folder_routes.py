import os
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FileFA, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from app.database.db import get_db
from app.middleware.auth_middleware import get_current_user
from app.middleware.pagination_middleware import get_pagination
from app.models import exceptions as ex
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.schemas import file_schemas
from app.schemas.file_schemas import FileBase
from app.services import file_services, folder_services
from app.schemas import folder_schemas
from app.core.limiter import limiter, FILE_RATE_LIMIT

folder_router = APIRouter()


@folder_router.get("", response_model=folder_schemas.PaginatedFolderResponse)
def get_folders(db: Session = Depends(get_db), usuario: User = Depends(get_current_user), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, carpetas = folder_services.obtener_carpetas_usuario_raiz_paginadas(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": [
            folder_schemas.FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                favorito=carpeta.favorito,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                id_carpeta=carpeta.id_carpeta,
                fecha_eliminacion=carpeta.fecha_eliminacion,
                fecha_favorito=carpeta.fecha_favorito
            )
            for carpeta in carpetas
        ],
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@folder_router.post("", response_model=folder_schemas.FolderResponse)
@limiter.limit(FILE_RATE_LIMIT)
def create_folder(request: Request, req: folder_schemas.FolderRequest, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        carpeta: Folder = folder_services.crear_carpeta(
            nombre=req.nombre_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta creada correctamente",
            "carpeta": folder_schemas.FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                favorito=carpeta.favorito,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                fecha_eliminacion=carpeta.fecha_eliminacion,
                fecha_favorito=carpeta.fecha_favorito
            )
        }
    except ex.IdYaUsadaException as e:
        raise HTTPException(409, str(e))
    except ex.NombreYaUsadoException as e2:
        raise HTTPException(409, str(e2))


@folder_router.get("/trash", response_model=folder_schemas.PaginatedFolderResponse)
def get_folders_trash(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, carpetas = folder_services.obtener_carpetas_papelera_raiz_paginadas(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": [
            folder_schemas.FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                favorito=carpeta.favorito,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                id_carpeta=carpeta.id_carpeta,
                fecha_eliminacion=carpeta.fecha_eliminacion,
                fecha_favorito=carpeta.fecha_favorito
            )
            for carpeta in carpetas
        ],
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@folder_router.delete("/trash/{id_carpeta}", response_model=folder_schemas.DeleteFolderPermanentResponse)
@limiter.limit(FILE_RATE_LIMIT)
def delete_folder_permanent(request: Request, id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        folder_services.eliminar_carpeta_permanente(
            id_carpeta=id_carpeta, db=db, usuario=usuario)

        return {
            "msg": "Carpeta eliminada correctamente"
        }
    except ex.CarpetaNoEncontradaException:
        raise HTTPException(
            404, detail="No se ha encontrado la carpeta en la papelera")
    except ex.EliminarDiscoException as e2:
        raise HTTPException(500, detail=str(e2))


@folder_router.get("/trash/{id_carpeta}/files", response_model=file_schemas.PaginatedFileResponse)
def get_files_of_folder_on_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    try:
        total, archivos = file_services.obtener_archivos_carpeta_papelera_paginados(
            id_carpeta=id_carpeta, usuario=usuario, db=db, pagina=pagina, limite=limite)

        return {
            "items": [
                file_schemas.FileBase(
                    id=archivo_db.id,
                    nombre_original=archivo_db.nombre_original,
                    path=archivo_db.path,
                    tamaño_bytes=archivo_db.tamaño_bytes,
                    favorito=archivo_db.favorito,
                    fecha_creacion=archivo_db.fecha_creacion,
                    id_usuario=archivo_db.id_usuario,
                    nombre_usuario=archivo_db.usuario.nombre,
                    id_carpeta=archivo_db.id_carpeta,
                    fecha_eliminacion=archivo_db.fecha_eliminacion,
                    fecha_favorito=archivo_db.fecha_favorito
                )
                for archivo_db in archivos
            ],
            "total": total,
            "pagina": pagina,
            "limite": limite
        }

    except ex.CarpetaNoEncontradaException:
        raise HTTPException(
            404, f"No se ha encontrado la carpeta con id {id_carpeta} en la papelera")


@folder_router.get("/trash/{id_carpeta}/folders", response_model=folder_schemas.PaginatedFolderResponse)
def get_folders_inside_folder_on_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    try:
        total, carpetas = folder_services.obtener_carpetas_carpeta_papelera_paginadas(
            id_carpeta=id_carpeta, usuario=usuario, db=db, pagina=pagina, limite=limite)

        return {
            "items": [
                folder_schemas.FolderBase(
                    id=carpeta.id,
                    nombre_original=carpeta.nombre_original,
                    path=carpeta.path,
                    favorito=carpeta.favorito,
                    fecha_creacion=carpeta.fecha_creacion,
                    id_usuario=carpeta.id_usuario,
                    nombre_usuario=carpeta.usuario.nombre,
                    id_carpeta=carpeta.id_carpeta,
                    fecha_eliminacion=carpeta.fecha_eliminacion,
                    fecha_favorito=carpeta.fecha_favorito
                )
                for carpeta in carpetas
            ],
            "total": total,
            "pagina": pagina,
            "limite": limite
        }

    except ex.CarpetaNoEncontradaException:
        raise HTTPException(
            404, detail=f"No se ha encontrado la carpeta con id {id_carpeta} en la papelera")


@folder_router.get("/{id_carpeta}", response_class=FileResponse)
def download_folder(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        zip_path, carpeta = folder_services.descargar_carpeta(
            id_carpeta=id_carpeta, usuario=usuario, db=db)

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename=f"{carpeta.nombre_original}.zip",
            background=BackgroundTask(lambda: os.remove(zip_path))
        )
    except ex.CarpetaNoEncontradaException as e1:
        raise HTTPException(404, detail=str(e1))


@folder_router.delete("/{id_carpeta}", response_model=folder_schemas.AddFolderTrashResponse)
@limiter.limit(FILE_RATE_LIMIT)
def add_folder_to_trash(request: Request, id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        carpeta: Folder = folder_services.añadir_carpeta_papelera(
            id_carpeta=id_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta enviada a la papelera con éxito",
            "carpeta": folder_schemas.FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                favorito=carpeta.favorito,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                fecha_eliminacion=carpeta.fecha_eliminacion,
                fecha_favorito=carpeta.fecha_favorito
            )
        }
    except ex.CarpetaPapeleraException:
        raise HTTPException(
            409, detail="La carpeta seleccionada ya está en la papelera")
    except ex.CarpetaNoEncontradaException:
        raise HTTPException(
            404, detail=f"No se ha encontrado la carpeta con ID {id_carpeta}")


@folder_router.put("/{id_carpeta}/restaurar", response_model=folder_schemas.RestoreFolderResponse)
def restore_folder_from_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        carpeta: Folder = folder_services.restaurar_carpeta_papelera(
            id_carpeta=id_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta restaurada correctamente",
            "carpeta": folder_schemas.FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                favorito=carpeta.favorito,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                fecha_eliminacion=carpeta.fecha_eliminacion,
                fecha_favorito=carpeta.fecha_favorito
            )
        }
    except ex.CarpetaNoEncontradaException as e1:
        raise HTTPException(404, str(e1))


@folder_router.get("/{id_carpeta}/files", response_model=file_schemas.PaginatedFileResponse)
def get_files_of_folder(id_carpeta: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    try:
        total, archivos = file_services.obtener_archivos_carpeta_paginados(
            id_carpeta=id_carpeta, db=db, usuario=usuario, pagina=pagina, limite=limite)

        return {
            "items": [
                file_schemas.FileBase(
                    id=archivo_db.id,
                    nombre_original=archivo_db.nombre_original,
                    path=archivo_db.path,
                    favorito=archivo_db.favorito,
                    tamaño_bytes=archivo_db.tamaño_bytes,
                    fecha_creacion=archivo_db.fecha_creacion,
                    id_usuario=archivo_db.id_usuario,
                    nombre_usuario=archivo_db.usuario.nombre,
                    id_carpeta=archivo_db.id_carpeta,
                    fecha_eliminacion=archivo_db.fecha_eliminacion,
                    fecha_favorito=archivo_db.fecha_favorito
                )
                for archivo_db in archivos
            ],
            "total": total,
            "pagina": pagina,
            "limite": limite
        }
    except ex.CarpetaNoEncontradaException:
        raise HTTPException(
            404, f"No se ha encontrado la carpeta con id {id_carpeta}")


@folder_router.post("/{id_carpeta}/files", response_model=folder_schemas.UploadFileFolderResponse)
async def upload_file_to_folder(id_carpeta: UUID, file_upload: list[UploadFile] = FileFA(...), db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivos: list[File] = []
        for file in file_upload:
            archivo_db: File = await folder_services.guardar_archivo_carpeta(id_carpeta=id_carpeta, file_upload=file, db=db, usuario=usuario)
            archivos.append(archivo_db)

        return {
            "msg": "Archivos subidos correctamente",
            "archivos": [
                FileBase(
                    id=archivo_guardado.id,
                    nombre_original=archivo_guardado.nombre_original,
                    path=archivo_guardado.path,
                    favorito=archivo_guardado.favorito,
                    tamaño_bytes=archivo_guardado.tamaño_bytes,
                    fecha_creacion=archivo_guardado.fecha_creacion,
                    id_usuario=archivo_guardado.id_usuario,
                    nombre_usuario=archivo_guardado.usuario.nombre,
                    id_carpeta=archivo_guardado.id_carpeta,
                    fecha_eliminacion=archivo_guardado.fecha_eliminacion,
                    fecha_favorito=archivo_guardado.fecha_favorito
                )
                for archivo_guardado in archivos
            ]
        }
    except ex.TamañoExcedidoException as e1:
        raise HTTPException(413, str(e1))
    except ex.CarpetaNoEncontradaException as e2:
        raise HTTPException(404, str(e2))
    except ex.NombreYaUsadoException as e3:
        raise HTTPException(409, str(e3))


@folder_router.get("/{id_carpeta}/folders", response_model=folder_schemas.PaginatedFolderResponse)
def get_folders_of_folder(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    try:
        total, carpetas = folder_services.obtener_carpetas_dentro_carpeta_paginadas(
            id_carpeta_padre=id_carpeta, usuario=usuario, db=db, pagina=pagina, limite=limite)

        return {
            "items": [
                folder_schemas.FolderBase(
                    id=carpeta.id,
                    nombre_original=carpeta.nombre_original,
                    path=carpeta.path,
                    favorito=carpeta.favorito,
                    fecha_creacion=carpeta.fecha_creacion,
                    id_usuario=carpeta.id_usuario,
                    nombre_usuario=carpeta.usuario.nombre,
                    id_carpeta=carpeta.id_carpeta,
                    fecha_eliminacion=carpeta.fecha_eliminacion,
                    fecha_favorito=carpeta.fecha_favorito
                )
                for carpeta in carpetas
            ],
            "total": total,
            "pagina": pagina,
            "limite": limite
        }
    except ex.CarpetaNoEncontradaException:
        raise HTTPException(
            404, f"No se ha encontrado la carpeta con id {id_carpeta}")


@folder_router.post("/{id_carpeta}/folders", response_model=folder_schemas.FolderResponse)
def create_folder_in_folder(id_carpeta: UUID, req: folder_schemas.FolderRequest, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        carpeta: Folder = folder_services.crear_carpeta_anidada(
            id_carpeta_padre=id_carpeta, nombre=req.nombre_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta creada correctamente",
            "carpeta": folder_schemas.FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                favorito=carpeta.favorito,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                id_carpeta=id_carpeta,
                fecha_eliminacion=carpeta.fecha_eliminacion,
                fecha_favorito=carpeta.fecha_favorito
            )
        }
    except ex.IdYaUsadaException as e:
        raise HTTPException(409, str(e))
    except ex.NombreYaUsadoException as e2:
        raise HTTPException(409, str(e2))
    except ex.CarpetaNoEncontradaException as e3:
        raise HTTPException(404, str(e3))
