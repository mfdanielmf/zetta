from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.limiter import limiter, FILE_RATE_LIMIT
from app.database.db import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas import multiple_schemas
from app.services import multiple_services
from app.models import exceptions as ex


multiple_router = APIRouter()


@multiple_router.put("/files/restaurar", response_model=multiple_schemas.MultipleFileResponse)
def restore_file_from_trash(ids_archivos: list[UUID], db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    try:
        errores = multiple_services.restaurar_multiples_archivos_papelera(
            ids=ids_archivos, usuario=usuario, db=db)

        if errores:
            return {
                "msg": "Proceso de restaurado completado",
                "items_totales": len(ids_archivos),
                "errores": {
                    "details": errores,
                    "total_errores": len(errores)
                }
            }

        return {
            "msg": "Proceso de restaurado completado",
            "items_totales": len(ids_archivos)
        }
    except ex.ArchivoNoEncontradoException:
        raise HTTPException(
            404, detail=f"No se ha encontrado el archivo en la papelera")


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
