from uuid import UUID

from pydantic import BaseModel


class ErrorItemMultiple(BaseModel):
    id_archivo: UUID
    nombre_archivo: str
    error: str


class ErroresMultiple(BaseModel):
    details: list[ErrorItemMultiple]
    total_errores: int


class DeleteMultiplePermanent(BaseModel):
    msg: str = "Proceso de eliminación completado"
    items_totales: int
    errores: ErroresMultiple | None = None
