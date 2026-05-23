from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth_middleware import get_current_user
from app.middleware.filters_middleware import get_filters
from app.middleware.pagination_middleware import get_pagination
from app.models.archivo_compartido import ArchivoCompartido
from app.models.archivo_favorito import ArchivoFavorito
from app.models.file import File
from app.models.folder import Folder
from app.models.user import User
from app.models import exceptions as ex
from app.services import item_services, favorite_services
from app.schemas import favorite_schemas, file_schemas, item_schemas, folder_schemas

item_router = APIRouter()


@item_router.get("", response_model=item_schemas.PaginatedItemResponse)
def get_items(
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    paginacion: tuple[int, int] = Depends(get_pagination),
    busqueda: str | None = Depends(get_filters)
):
    pagina, limite = paginacion

    total, items = item_services.obtener_items_raiz_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite, busqueda=busqueda)

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
                    fecha_eliminacion=item.fecha_eliminacion,
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
                    fecha_eliminacion=item.fecha_eliminacion,
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@item_router.get("/{id_carpeta}/items", response_model=item_schemas.PaginatedItemResponse)
def get_items_folder(
    id_carpeta: UUID,
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    paginacion: tuple[int, int] = Depends(get_pagination),
    busqueda: str | None = Depends(get_filters)
):
    pagina, limite = paginacion

    try:
        total, items = item_services.obtener_items_carpeta_paginados(id_carpeta=id_carpeta,
                                                                     usuario=usuario, db=db, pagina=pagina, limite=limite, busqueda=busqueda)

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
                        fecha_eliminacion=item.fecha_eliminacion,
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
                        fecha_eliminacion=item.fecha_eliminacion,
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
def get_items_trash(
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    paginacion: tuple[int, int] = Depends(get_pagination),
    busqueda: str | None = Depends(get_filters)
):
    pagina, limite = paginacion

    total, items = item_services.obtener_items_papelera_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite, busqueda=busqueda)

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
                    fecha_eliminacion=item.fecha_eliminacion,
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
                    fecha_eliminacion=item.fecha_eliminacion,
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@item_router.get("/trash/{id_carpeta}/items", response_model=item_schemas.PaginatedItemResponse)
def get_items_folder_in_trash(
    id_carpeta: UUID,
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    paginacion: tuple[int, int] = Depends(get_pagination),
    busqueda: str | None = Depends(get_filters)
):
    pagina, limite = paginacion

    try:
        total, items = item_services.obtener_items_carpeta_papelera_paginados(id_carpeta=id_carpeta,
                                                                              usuario=usuario, db=db, pagina=pagina, limite=limite, busqueda=busqueda)

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
                        fecha_eliminacion=item.fecha_eliminacion,
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
                        fecha_eliminacion=item.fecha_eliminacion,
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


@item_router.get("/shared/sent", response_model=item_schemas.PaginatedSharedItemResponse)
def get_sent_items(
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    paginacion: tuple[int, int] = Depends(get_pagination),
    busqueda: str | None = Depends(get_filters)
):
    pagina, limite = paginacion

    total, items = item_services.obtener_items_compartidos_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite, busqueda=busqueda)

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
                        fecha_eliminacion=item.archivo.fecha_eliminacion,
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
                        fecha_eliminacion=item.carpeta.fecha_eliminacion,
                    )
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@item_router.get("/shared/received", response_model=item_schemas.PaginatedSharedItemResponse)
def get_received_items(
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    paginacion: tuple[int, int] = Depends(get_pagination),
    busqueda: str | None = Depends(get_filters)
):
    pagina, limite = paginacion

    total, items = item_services.obtener_items_recibidos_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite, busqueda=busqueda)

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
                        fecha_eliminacion=item.archivo.fecha_eliminacion,
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
                        fecha_eliminacion=item.carpeta.fecha_eliminacion,
                    )
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@item_router.get("/favorite", response_model=item_schemas.PaginatedFavoriteItemReponse)
def get_favorite_items(
    usuario: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    paginacion: tuple[int, int] = Depends(get_pagination),
    busqueda: str | None = Depends(get_filters)
):
    pagina, limite = paginacion

    total, items = favorite_services.obtener_items_favoritos(
        db=db, usuario=usuario, pagina=pagina, limite=limite, busqueda=busqueda)

    items_serializados: list[Union[file_schemas.FileBase,
                                   file_schemas.File]] = []

    for item in items:
        if isinstance(item, ArchivoFavorito):
            archivo: File = item.archivo

            items_serializados.append(
                favorite_schemas.FavoriteFileBase(
                    id=item.id,
                    fecha_favorito=item.fecha_favorito,
                    usuario=item.usuario,
                    archivo=file_schemas.FileBase(
                        id=archivo.id,
                        nombre_original=archivo.nombre_original,
                        path=archivo.path,
                        tamaño_bytes=archivo.tamaño_bytes,
                        fecha_creacion=archivo.fecha_creacion,
                        id_usuario=archivo.id_usuario,
                        nombre_usuario=archivo.usuario.nombre,
                        id_carpeta=archivo.id_carpeta,
                        fecha_eliminacion=archivo.fecha_eliminacion,
                    )
                )
            )
        else:
            carpeta: Folder = item.carpeta

            items_serializados.append(
                favorite_schemas.FavoriteFolderBase(
                    id=item.id,
                    fecha_favorito=item.fecha_favorito,
                    usuario=item.usuario,
                    carpeta=folder_schemas.FolderBase(
                        id=carpeta.id,
                        nombre_original=carpeta.nombre_original,
                        path=carpeta.path,
                        fecha_creacion=carpeta.fecha_creacion,
                        id_usuario=carpeta.id_usuario,
                        nombre_usuario=carpeta.usuario.nombre,
                        id_carpeta=carpeta.id_carpeta,
                        fecha_eliminacion=carpeta.fecha_eliminacion,
                    )
                )
            )

    return {
        "items": items_serializados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }
