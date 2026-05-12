from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr


class ItemMultipleRequest(BaseModel):
    id: UUID
    tipo: Literal["archivo", "carpeta"]


class ShareMultipleItemsRequest(BaseModel):
    correo_usuario: EmailStr
    items: list[ItemMultipleRequest]


class ErrorItemMultiple(BaseModel):
    id_item: UUID
    nombre_item: str
    error: str


class ErroresMultiple(BaseModel):
    details: list[ErrorItemMultiple]
    total_errores: int


class MultipleItemResponse(BaseModel):
    msg: str
    items_totales: int
    errores: ErroresMultiple | None = None
