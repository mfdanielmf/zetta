from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FileFA
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.exceptions import CarpetaPapeleraException, EliminarDiscoException, IdYaUsadaException, NombreYaUsadoException, TamañoExcedidoException, CarpetaNoEncontradaException
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.schemas.file_schemas import FileBase
from app.services.file_services import obtener_archivos_carpeta, obtener_archivos_carpeta_papelera
from app.services.auth_services import get_current_user
from app.services.folder_services import crear_carpeta, descargar_carpeta, eliminar_carpeta_permanente, obtener_carpetas_usuario_raiz, guardar_archivo_carpeta, crear_carpeta_anidada, obtener_carpetas_dentro_carpeta, añadir_carpeta_papelera, restaurar_carpeta_papelera, obtener_carpetas_papelera_raiz, obtener_carpetas_carpeta_papelera
from app.schemas.folder_schemas import DeleteFolderPermanentResponse, FolderBase, FolderRequest, FolderResponse, RestoreFolderResponse, UploadFileFolderResponse, AddFolderTrashResponse

folder_router = APIRouter()


@folder_router.get("", response_model=list[FolderBase])
def get_folders(db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    carpetas: list[Folder] = obtener_carpetas_usuario_raiz(
        usuario=usuario, db=db)

    return [
        FolderBase(
            id=carpeta.id,
            nombre_original=carpeta.nombre_original,
            path=carpeta.path,
            fecha_creacion=carpeta.fecha_creacion,
            id_usuario=carpeta.id_usuario,
            nombre_usuario=carpeta.usuario.nombre,
            id_carpeta=carpeta.id_carpeta,
            fecha_eliminacion=carpeta.fecha_eliminacion
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
                nombre_usuario=carpeta.usuario.nombre,
                fecha_eliminacion=carpeta.fecha_eliminacion
            )
        }
    except IdYaUsadaException as e:
        raise HTTPException(409, str(e))
    except NombreYaUsadoException as e2:
        raise HTTPException(409, str(e2))


@folder_router.get("/trash", response_model=list[FolderBase])
def get_folders_trash(usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    carpetas: list[Folder] = obtener_carpetas_papelera_raiz(
        usuario=usuario, db=db)

    return [
        FolderBase(
            id=carpeta.id,
            nombre_original=carpeta.nombre_original,
            path=carpeta.path,
            fecha_creacion=carpeta.fecha_creacion,
            id_usuario=carpeta.id_usuario,
            nombre_usuario=carpeta.usuario.nombre,
            id_carpeta=carpeta.id_carpeta,
            fecha_eliminacion=carpeta.fecha_eliminacion
        )
        for carpeta in carpetas
    ]


@folder_router.delete("/trash/{id_carpeta}", response_model=DeleteFolderPermanentResponse)
def delete_folder_permanent(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        eliminar_carpeta_permanente(
            id_carpeta=id_carpeta, db=db, usuario=usuario)

        return {
            "msg": "Carpeta eliminada correctamente"
        }
    except CarpetaNoEncontradaException:
        raise HTTPException(
            404, detail="No se ha encontrado la carpeta en la papelera")
    except EliminarDiscoException as e2:
        raise HTTPException(500, detail=str(e2))


@folder_router.get("/trash/{id_carpeta}/files", response_model=list[FileBase])
def get_files_of_folder_on_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        archivos: list[File] = obtener_archivos_carpeta_papelera(
            db=db, id_carpeta=id_carpeta, usuario=usuario)

        return [
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
            )
            for archivo in archivos
        ]
    except CarpetaNoEncontradaException:
        raise HTTPException(
            404, f"No se ha encontrado la carpeta con id {id_carpeta} en la papelera")


@folder_router.get("/trash/{id_carpeta}/folders", response_model=list[FolderBase])
def get_folders_inside_folder_on_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        carpetas: list[Folder] = obtener_carpetas_carpeta_papelera(
            id_carpeta=id_carpeta, usuario=usuario, db=db)

        return [
            FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                id_carpeta=carpeta.id_carpeta,
                fecha_eliminacion=carpeta.fecha_eliminacion
            )
            for carpeta in carpetas
        ]
    except CarpetaNoEncontradaException:
        raise HTTPException(
            404, detail=f"No se ha encontrado la carpeta con id {id_carpeta} en la papelera")


@folder_router.get("/{id_carpeta}")
def download_folder(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        buffer, carpeta = descargar_carpeta(
            id_carpeta=id_carpeta, usuario=usuario, db=db)

        return StreamingResponse(
            content=buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{carpeta.nombre_original}.zip"'
            }
        )
    except CarpetaNoEncontradaException as e1:
        raise HTTPException(404, detail=str(e1))


@folder_router.delete("/{id_carpeta}", response_model=AddFolderTrashResponse)
def add_folder_to_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        carpeta: Folder = añadir_carpeta_papelera(
            id_carpeta=id_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta enviada a la papelera con éxito",
            "carpeta": FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                fecha_eliminacion=carpeta.fecha_eliminacion
            )
        }
    except CarpetaPapeleraException:
        raise HTTPException(
            409, detail="La carpeta seleccionada ya está en la papelera")
    except CarpetaNoEncontradaException:
        raise HTTPException(
            404, detail=f"No se ha encontrado la carpeta con ID {id_carpeta}")


@folder_router.put("/{id_carpeta}/restaurar", response_model=RestoreFolderResponse)
def restore_folder_from_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        carpeta: Folder = restaurar_carpeta_papelera(
            id_carpeta=id_carpeta, usuario=usuario, db=db)

        return {
            "msg": "Carpeta restaurada correctamente",
            "carpeta": FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                fecha_eliminacion=carpeta.fecha_eliminacion
            )
        }
    except CarpetaNoEncontradaException as e1:
        raise HTTPException(404, str(e1))


@folder_router.get("/{id_carpeta}/files", response_model=list[FileBase])
def get_files_of_folder(id_carpeta: UUID, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        archivos: list[File] = obtener_archivos_carpeta(
            db=db, id_carpeta=id_carpeta, usuario=usuario)

        return [
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
            )
            for archivo in archivos
        ]
    except CarpetaNoEncontradaException:
        raise HTTPException(
            404, f"No se ha encontrado la carpeta con id {id_carpeta}")


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
                    id_carpeta=archivo_guardado.id_carpeta,
                    fecha_eliminacion=archivo_guardado.fecha_eliminacion
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


@folder_router.get("/{id_carpeta}/folders", response_model=list[FolderBase])
def get_folders_of_folder(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        carpetas: list[Folder] = obtener_carpetas_dentro_carpeta(
            id_carpeta_padre=id_carpeta, usuario=usuario, db=db)

        return [
            FolderBase(
                id=carpeta.id,
                nombre_original=carpeta.nombre_original,
                path=carpeta.path,
                fecha_creacion=carpeta.fecha_creacion,
                id_usuario=carpeta.id_usuario,
                nombre_usuario=carpeta.usuario.nombre,
                id_carpeta=carpeta.id_carpeta,
                fecha_eliminacion=carpeta.fecha_eliminacion
            )
            for carpeta in carpetas
        ]
    except CarpetaNoEncontradaException:
        raise HTTPException(
            404, f"No se ha encontrado la carpeta con id {id_carpeta}")


@folder_router.post("/{id_carpeta}/folders", response_model=FolderResponse)
def create_folder_in_folder(id_carpeta: UUID, req: FolderRequest, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
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
                id_carpeta=id_carpeta,
                fecha_eliminacion=carpeta.fecha_eliminacion
            )
        }
    except IdYaUsadaException as e:
        raise HTTPException(409, str(e))
    except NombreYaUsadoException as e2:
        raise HTTPException(409, str(e2))
    except CarpetaNoEncontradaException as e3:
        raise HTTPException(404, str(e3))
