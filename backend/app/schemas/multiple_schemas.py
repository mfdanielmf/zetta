from uuid import UUID

from pydantic import BaseModel


class ErrorItemMultiple(BaseModel):
    id_item: UUID
    nombre_item: str
    error: str


class ErroresMultiple(BaseModel):
    details: list[ErrorItemMultiple]
    total_errores: int


class MultipleFileResponse(BaseModel):
    msg: str
    items_totales: int
    errores: ErroresMultiple | None = None
