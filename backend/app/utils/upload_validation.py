from fastapi import UploadFile

from app.config import config
from app.models.exceptions import TipoArchivoNoPermitidoException


def validar_archivo(file_upload: UploadFile) -> None:
    """
    TipoArchivoNoPermitidoException
    """
    nombre: str = file_upload.filename or ""

    extension: str = nombre.rsplit(".", 1)[-1].lower().strip() if "." in nombre else ""

    if not extension:
        raise TipoArchivoNoPermitidoException("El archivo no tiene extensión")

    if extension not in config.ALLOWED_EXTENSIONS:
        raise TipoArchivoNoPermitidoException(f"Extensión '.{extension}' no permitida")
