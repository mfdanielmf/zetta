from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.limiter import DEFAULT_RATE_LIMIT, limiter, FILE_RATE_LIMIT
from app.database.db import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.models import exceptions as ex
from app.schemas import multiple_schemas
from app.services import multiple_services


multiple_router = APIRouter()


@multiple_router.delete("/items", response_model=multiple_schemas.MultipleFileResponse)
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


@multiple_router.put("/items/restaurar", response_model=multiple_schemas.MultipleFileResponse)
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


@multiple_router.delete("/items/trash", response_model=multiple_schemas.MultipleFileResponse)
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


@multiple_router.post("/sent/items", response_model=multiple_schemas.MultipleFileResponse)
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
