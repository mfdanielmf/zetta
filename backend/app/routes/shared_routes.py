from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.archivo_compartido import ArchivoCompartido
from app.models.exceptions import ArchivoNoEncontradoException, PropietarioException, UsuarioNoEncontradoException, YaCompartidoException
from app.models.user import User
from app.schemas import shared_file_schemas
from app.schemas.file_schemas import FileBase
from app.services.auth_services import get_current_user
from app.services import shared_file_services

shared_router = APIRouter()


@shared_router.post("/files", response_model=shared_file_schemas.ShareFileResponse)
def share_file(req: shared_file_schemas.ShareFileRequest, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        archivo_compartido: ArchivoCompartido = shared_file_services.compartir_archivo(
            req=req, usuario=usuario, db=db)

        return {
            "msg": "Archivo compartido con éxito",
            "archivo_compartido": {
                "id": archivo_compartido.id,
                "fecha_compartido": archivo_compartido.fecha_compartido,
                "propietario": archivo_compartido.propietario,
                "receptor": archivo_compartido.receptor,
                "archivo": FileBase(
                    id=archivo_compartido.archivo.id,
                    nombre_original=archivo_compartido.archivo.nombre_original,
                    path=archivo_compartido.archivo.path,
                    tamaño_bytes=archivo_compartido.archivo.tamaño_bytes,
                    fecha_creacion=archivo_compartido.archivo.fecha_creacion,
                    id_usuario=archivo_compartido.archivo.id_usuario,
                    nombre_usuario=archivo_compartido.archivo.usuario.nombre,
                    id_carpeta=archivo_compartido.archivo.id_carpeta,
                    fecha_eliminacion=archivo_compartido.archivo.fecha_eliminacion
                )
            }
        }

    except UsuarioNoEncontradoException as e1:
        raise HTTPException(404, detail=str(e1))
    except ArchivoNoEncontradoException as e2:
        raise HTTPException(404, detail=str(e2))
    except PropietarioException as e3:
        raise HTTPException(400, detail=str(e3))
    except YaCompartidoException as e4:
        raise HTTPException(409, detail=str(e4))
