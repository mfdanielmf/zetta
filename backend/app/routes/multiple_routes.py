import os

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from app.core.limiter import DEFAULT_RATE_LIMIT, limiter, FILE_RATE_LIMIT
from app.database.db import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.models import exceptions as ex
from app.schemas import multiple_schemas
from app.services import multiple_services


multiple_router = APIRouter()


@multiple_router.delete("/items", response_model=multiple_schemas.MultipleItemResponse)
@limiter.limit(FILE_RATE_LIMIT)
def add_multiple_items_to_trash(req: list[multiple_schemas.ItemMultipleRequest], request: Request, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    errores = multiple_services.añadir_multiples_items_papelera(
        items=req, usuario=usuario, db=db)

    if errores:
        return {
            "msg": "Proceso de eliminación completado",
            "items_totales": len(req),
            "errores": {
                "details": errores,
                "total_errores": len(errores)
            }
        }

    return {
        "msg": "Proceso de eliminación completado",
        "items_totales": len(req)
    }


@multiple_router.put("/items/restaurar", response_model=multiple_schemas.MultipleItemResponse)
def restore_items_from_trash(req: list[multiple_schemas.ItemMultipleRequest], db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    errores = multiple_services.restaurar_multiples_items_papelera(
        items=req, usuario=usuario, db=db)

    if errores:
        return {
            "msg": "Proceso de restaurado completado",
            "items_totales": len(req),
            "errores": {
                "details": errores,
                "total_errores": len(errores)
            }
        }

    return {
        "msg": "Proceso de restaurado completado",
        "items_totales": len(req)
    }


@multiple_router.delete("/items/trash", response_model=multiple_schemas.MultipleItemResponse)
@limiter.limit(FILE_RATE_LIMIT)
def delete_multiple_items_permanent(req: list[multiple_schemas.ItemMultipleRequest], request: Request, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    errores = multiple_services.eliminar_multiples_items_permanente(
        items=req, usuario=usuario, db=db)

    if errores:
        return {
            "msg": "Proceso de eliminación completado",
            "items_totales": len(req),
            "errores": {
                "details": errores,
                "total_errores": len(errores)
            }
        }

    return {
        "msg": "Proceso de eliminación completado",
        "items_totales": len(req)
    }


@multiple_router.post("/items/sent", response_model=multiple_schemas.MultipleItemResponse)
@limiter.limit(DEFAULT_RATE_LIMIT)
def share_multiple_items_with_user(req: multiple_schemas.ShareMultipleItemsRequest, request: Request, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        errores = multiple_services.compartir_multiples_items(
            req=req, usuario=usuario, db=db)

        if errores:
            return {
                "msg": "Proceso de compartido completado",
                "items_totales": len(req.items),
                "errores": {
                    "details": errores,
                    "total_errores": len(errores)
                }
            }

        return {
            "msg": "Proceso de compartido completado",
            "items_totales": len(req.items)
        }
    except ex.UsuarioNoEncontradoException as e1:
        raise HTTPException(404, detail=str(e1))
    except ex.PropietarioException as e2:
        raise HTTPException(400, detail=str(e2))


@multiple_router.delete("/items/shared/sent", response_model=multiple_schemas.MultipleItemResponse)
@limiter.limit(DEFAULT_RATE_LIMIT)
def cancel_multiple_shared_items(req: list[multiple_schemas.ItemMultipleRequest], request: Request, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        errores = multiple_services.cancelar_multiples_compartidos(
            req=req, usuario=usuario, db=db)

        if errores:
            return {
                "msg": "Proceso de cancelación completado",
                "items_totales": len(req),
                "errores": {
                    "details": errores,
                    "total_errores": len(errores)
                }
            }

        return {
            "msg": "Proceso de cancelación completado",
            "items_totales": len(req)
        }
    except ex.UsuarioNoEncontradoException as e1:
        raise HTTPException(404, detail=str(e1))
    except ex.PropietarioException as e2:
        raise HTTPException(400, detail=str(e2))


@multiple_router.post("/items", response_class=FileResponse)
def download_multiple_items_zip(req: list[multiple_schemas.ItemMultipleRequest], db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        zip_path: str = multiple_services.descargar_multiples_items(
            items=req, usuario=usuario, db=db)

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename="zetta_descarga.zip",
            background=BackgroundTask(lambda: os.remove(zip_path))
        )
    except ex.ArchivoNoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ex.CarpetaNoEncontradaException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error interno al descargar los items")


@multiple_router.put("/items/favorite", response_model=multiple_schemas.MultipleItemResponse)
@limiter.limit(DEFAULT_RATE_LIMIT)
def toggle_favorite_item(req: list[multiple_schemas.ItemMultipleRequest], request: Request, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        errores = multiple_services.toggle_multiples_favoritos(
            req=req, usuario=usuario, db=db)

        if errores:
            return {
                "msg": "Proceso de favoritos completado",
                "items_totales": len(req),
                "errores": {
                    "details": errores,
                    "total_errores": len(errores)
                }
            }

        return {
            "msg": "Proceso de favoritos completado",
            "items_totales": len(req)
        }

    except Exception:
        raise HTTPException(500, detail="Error interno al modificar favoritos")
