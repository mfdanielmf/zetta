from uuid import UUID

from pydantic import BaseModel


class ErrorFileMultiple(BaseModel):
    id_archivo: UUID
    nombre_archivo: str
    error: str


class ErroresFileMultiple(BaseModel):
    details: list[ErrorFileMultiple]
    total_errores: int


class MultipleFileResponse(BaseModel):
    msg: str
    items_totales: int
    errores: ErroresFileMultiple | None = None
