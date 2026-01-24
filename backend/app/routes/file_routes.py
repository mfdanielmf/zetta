from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.services.file_services import guardar_archivo
from app.models.exceptions import TamañoExcedidoException, IdYaUsadaException
from app.schemas.file_schemas import FileBase, FileResponse

file_router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@file_router.post("/", response_model=FileResponse)
async def upload_file(file_upload: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        archivo_db: File = await guardar_archivo(file_upload=file_upload, db=db)

        return {
            "msg": "Archivo guardado con éxito",
            "archivo": FileBase.model_validate(archivo_db)
        }
    except TamañoExcedidoException as e1:
        raise HTTPException(413, str(e1))
    except IdYaUsadaException as e2:
        raise HTTPException(409, str(e2))
