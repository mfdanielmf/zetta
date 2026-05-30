from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.middleware.auth_middleware import get_current_user
from app.database.db import get_db
from app.middleware.pagination_middleware import get_pagination
from app.models.archivo_compartido import ArchivoCompartido
from app.models.carpeta_compartida import CarpetaCompartida
from app.models import exceptions as ex
from app.models.user import User
from app.schemas import shared_file_schemas, shared_folder_schemas, file_schemas, folder_schemas
from app.services import shared_file_services, shared_folder_services
from app.core.limiter import limiter, DEFAULT_RATE_LIMIT

shared_router = APIRouter()


@shared_router.get("/sent/files", response_model=shared_file_schemas.PaginatedSharedFileResponse)
def get_shared_files_by_user(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, archivos_paginados = shared_file_services.obtener_archivos_compartidos_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": archivos_paginados,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@shared_router.post("/sent/files", response_model=shared_file_schemas.ShareFileResponse)
@limiter.limit(DEFAULT_RATE_LIMIT)
def share_file_with_user(request: Request, req: shared_file_schemas.ShareFileRequest, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
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
                "archivo": file_schemas.FileBase(
                    id=archivo_compartido.archivo.id,
                    nombre_original=archivo_compartido.archivo.nombre_original,
                    path=archivo_compartido.archivo.path,
                    tamaño_bytes=archivo_compartido.archivo.tamaño_bytes,
                    fecha_creacion=archivo_compartido.archivo.fecha_creacion,
                    id_usuario=archivo_compartido.archivo.id_usuario,
                    nombre_usuario=archivo_compartido.archivo.usuario.nombre,
                    id_carpeta=archivo_compartido.archivo.id_carpeta,
                    fecha_eliminacion=archivo_compartido.archivo.fecha_eliminacion,
                )
            }
        }

    except ex.UsuarioNoEncontradoException as e1:
        raise HTTPException(404, detail=str(e1))
    except ex.ArchivoNoEncontradoException as e2:
        raise HTTPException(404, detail=str(e2))
    except ex.PropietarioException as e3:
        raise HTTPException(400, detail=str(e3))
    except ex.YaCompartidoException as e4:
        raise HTTPException(409, detail=str(e4))


@shared_router.get("/sent/folders", response_model=shared_folder_schemas.PaginatedSharedFolderResponse)
def get_shared_folders_by_user(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, carpetas_paginadas = shared_folder_services.obtener_carpetas_compartidas_paginadas(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": carpetas_paginadas,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@shared_router.post("/sent/folders", response_model=shared_folder_schemas.ShareFolderResponse)
@limiter.limit(DEFAULT_RATE_LIMIT)
def share_folder_with_user(request: Request, req: shared_folder_schemas.ShareFolderRequest, usuario: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        carpeta_compartida: CarpetaCompartida = shared_folder_services.compartir_carpeta(
            req=req, usuario=usuario, db=db)

        return {
            "msg": "Carpeta compartida con éxito",
            "carpeta_compartida": {
                "id": carpeta_compartida.id,
                "fecha_compartido": carpeta_compartida.fecha_compartido,
                "propietario": carpeta_compartida.propietario,
                "receptor": carpeta_compartida.receptor,
                "carpeta": folder_schemas.FolderBase(
                    id=carpeta_compartida.carpeta.id,
                    nombre_original=carpeta_compartida.carpeta.nombre_original,
                    path=carpeta_compartida.carpeta.path,
                    fecha_creacion=carpeta_compartida.carpeta.fecha_creacion,
                    id_usuario=carpeta_compartida.carpeta.id_usuario,
                    nombre_usuario=carpeta_compartida.carpeta.usuario.nombre,
                    id_carpeta=carpeta_compartida.carpeta.id_carpeta,
                    fecha_eliminacion=carpeta_compartida.carpeta.fecha_eliminacion,
                )
            }
        }

    except ex.UsuarioNoEncontradoException as e1:
        raise HTTPException(404, detail=str(e1))
    except ex.CarpetaNoEncontradaException as e2:
        raise HTTPException(404, detail=str(e2))
    except ex.PropietarioException as e3:
        raise HTTPException(400, detail=str(e3))
    except ex.YaCompartidoException as e4:
        raise HTTPException(409, detail=str(e4))


@shared_router.get("/received/files", response_model=shared_file_schemas.PaginatedSharedFileResponse)
def get_shared_files_with_user(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, archivos_recibidos = shared_file_services.obtener_archivos_compartidos_paginados(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": archivos_recibidos,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }


@shared_router.get("/received/folders", response_model=shared_folder_schemas.PaginatedSharedFolderResponse)
def get_shared_folders_by_user(usuario: User = Depends(get_current_user), db: Session = Depends(get_db), paginacion: tuple[int, int] = Depends(get_pagination)):
    pagina, limite = paginacion

    total, carpetas_recibidas = shared_folder_services.obtener_carpetas_recibidas_paginadas(
        usuario=usuario, db=db, pagina=pagina, limite=limite)

    return {
        "items": carpetas_recibidas,
        "total": total,
        "pagina": pagina,
        "limite": limite
    }
