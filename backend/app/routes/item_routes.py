from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth_middleware import get_current_user
from app.middleware.pagination_middleware import get_pagination
from app.models.archivo_compartido import ArchivoCompartido
from app.models.file import File
from app.models.user import User
from app.models import exceptions as ex
from app.services import item_services
from app.schemas import file_schemas, item_schemas, folder_schemas

item_router = APIRouter()


@item_router.get("", response_model=item_schemas.PaginatedItemResponse)
def get_items(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, items = item_services.obtener_items_raiz_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    items_serializados: list[Union[file_schemas.FileBase,
                                   file_schemas.File]] = []

    for item in items:
        if isinstance(item, File):
            items_serializados.append(
                item_schemas.FileItem(
                    id=item.id,
                    nombre_original=item.nombre_original,
                    path=item.path,
                    tamaño_bytes=item.tamaño_bytes,
                    fecha_creacion=item.fecha_creacion,
                    id_usuario=item.id_usuario,
                    nombre_usuario=item.usuario.nombre,
                    id_carpeta=item.id_carpeta,
                    fecha_eliminacion=item.fecha_eliminacion
                )
            )
        else:
            items_serializados.append(
                item_schemas.FolderItem(
                    id=item.id,
                    nombre_original=item.nombre_original,
                    path=item.path,
                    fecha_creacion=item.fecha_creacion,
                    id_usuario=item.id_usuario,
                    nombre_usuario=item.usuario.nombre,
                    id_carpeta=item.id_carpeta,
                    fecha_eliminacion=item.fecha_eliminacion
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@item_router.get("/{id_carpeta}/items", response_model=item_schemas.PaginatedItemResponse)
def get_items_folder(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    try:
        total, items = item_services.obtener_items_carpeta_paginados(id_carpeta=id_carpeta,
                                                                     usuario=usuario, db=db, pagina=pagina, limite=limite)

        items_serializados: list[Union[file_schemas.FileBase,
                                       file_schemas.File]] = []

        for item in items:
            if isinstance(item, File):
                items_serializados.append(
                    item_schemas.FileItem(
                        id=item.id,
                        nombre_original=item.nombre_original,
                        path=item.path,
                        tamaño_bytes=item.tamaño_bytes,
                        fecha_creacion=item.fecha_creacion,
                        id_usuario=item.id_usuario,
                        nombre_usuario=item.usuario.nombre,
                        id_carpeta=item.id_carpeta,
                        fecha_eliminacion=item.fecha_eliminacion
                    )
                )
            else:
                items_serializados.append(
                    item_schemas.FolderItem(
                        id=item.id,
                        nombre_original=item.nombre_original,
                        path=item.path,
                        fecha_creacion=item.fecha_creacion,
                        id_usuario=item.id_usuario,
                        nombre_usuario=item.usuario.nombre,
                        id_carpeta=item.id_carpeta,
                        fecha_eliminacion=item.fecha_eliminacion
                    )
                )

        return {
            "items": items_serializados,
            "total": total,
            "pagina": pagina,
            "limite": limite
        }

    except ex.CarpetaNoEncontradaException as e1:
        raise HTTPException(404, detail=str(e1))


@item_router.get("/trash", response_model=item_schemas.PaginatedItemResponse)
def get_items_trash(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, items = item_services.obtener_items_papelera_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    items_serializados: list[Union[file_schemas.FileBase,
                                   file_schemas.File]] = []

    for item in items:
        if isinstance(item, File):
            items_serializados.append(
                item_schemas.FileItem(
                    id=item.id,
                    nombre_original=item.nombre_original,
                    path=item.path,
                    tamaño_bytes=item.tamaño_bytes,
                    fecha_creacion=item.fecha_creacion,
                    id_usuario=item.id_usuario,
                    nombre_usuario=item.usuario.nombre,
                    id_carpeta=item.id_carpeta,
                    fecha_eliminacion=item.fecha_eliminacion
                )
            )
        else:
            items_serializados.append(
                item_schemas.FolderItem(
                    id=item.id,
                    nombre_original=item.nombre_original,
                    path=item.path,
                    fecha_creacion=item.fecha_creacion,
                    id_usuario=item.id_usuario,
                    nombre_usuario=item.usuario.nombre,
                    id_carpeta=item.id_carpeta,
                    fecha_eliminacion=item.fecha_eliminacion
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@item_router.get("/trash/{id_carpeta}/items", response_model=item_schemas.PaginatedItemResponse)
def get_items_folder_in_trash(id_carpeta: UUID, usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    try:
        total, items = item_services.obtener_items_carpeta_papelera_paginados(id_carpeta=id_carpeta,
                                                                              usuario=usuario, db=db, pagina=pagina, limite=limite)

        items_serializados: list[Union[file_schemas.FileBase,
                                       file_schemas.File]] = []

        for item in items:
            if isinstance(item, File):
                items_serializados.append(
                    item_schemas.FileItem(
                        id=item.id,
                        nombre_original=item.nombre_original,
                        path=item.path,
                        tamaño_bytes=item.tamaño_bytes,
                        fecha_creacion=item.fecha_creacion,
                        id_usuario=item.id_usuario,
                        nombre_usuario=item.usuario.nombre,
                        id_carpeta=item.id_carpeta,
                        fecha_eliminacion=item.fecha_eliminacion
                    )
                )
            else:
                items_serializados.append(
                    item_schemas.FolderItem(
                        id=item.id,
                        nombre_original=item.nombre_original,
                        path=item.path,
                        fecha_creacion=item.fecha_creacion,
                        id_usuario=item.id_usuario,
                        nombre_usuario=item.usuario.nombre,
                        id_carpeta=item.id_carpeta,
                        fecha_eliminacion=item.fecha_eliminacion
                    )
                )

        return {
            "items": items_serializados,
            "total": total,
            "pagina": pagina,
            "limite": limite
        }

    except ex.CarpetaNoEncontradaException:
        raise HTTPException(
            404, detail=f"No se ha encontrado la carpeta con id {id_carpeta} en la papelera")


@item_router.get("/sent", response_model=item_schemas.PaginatedSharedItemResponse)
def get_sent_items(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, items = item_services.obtener_items_compartidos_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    items_serializados: list[Union[file_schemas.FileBase,
                                   file_schemas.File]] = []

    for item in items:
        if isinstance(item, ArchivoCompartido):
            items_serializados.append(
                item_schemas.SharedFileItem(
                    id=item.id,
                    fecha_compartido=item.fecha_compartido,
                    propietario=item.propietario,
                    receptor=item.receptor,
                    archivo=file_schemas.FileBase(
                        id=item.archivo.id,
                        nombre_original=item.archivo.nombre_original,
                        path=item.archivo.path,
                        tamaño_bytes=item.archivo.tamaño_bytes,
                        fecha_creacion=item.archivo.fecha_creacion,
                        id_usuario=item.archivo.id_usuario,
                        nombre_usuario=item.archivo.usuario.nombre,
                        id_carpeta=item.archivo.id_carpeta,
                        fecha_eliminacion=item.archivo.fecha_eliminacion
                    )
                )
            )
        else:
            items_serializados.append(
                item_schemas.SharedFolderItem(
                    id=item.id,
                    fecha_compartido=item.fecha_compartido,
                    propietario=item.propietario,
                    receptor=item.receptor,
                    carpeta=folder_schemas.FolderBase(
                        id=item.carpeta.id,
                        nombre_original=item.carpeta.nombre_original,
                        path=item.carpeta.path,
                        fecha_creacion=item.carpeta.fecha_creacion,
                        id_usuario=item.carpeta.id_usuario,
                        nombre_usuario=item.carpeta.usuario.nombre,
                        id_carpeta=item.carpeta.id_carpeta,
                        fecha_eliminacion=item.carpeta.fecha_eliminacion
                    )
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }
