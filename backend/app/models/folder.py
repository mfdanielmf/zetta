import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.db import Base


class Folder(Base):
    __tablename__ = "carpetas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_original = Column(String(100), nullable=False)
    path = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())

    id_usuario = Column(UUID(as_uuid=True), ForeignKey(
        "usuarios.id"), nullable=False)
    id_carpeta = Column(UUID(as_uuid=True), ForeignKey(
        "carpetas.id"), nullable=True)

    usuario = relationship(
        "User", back_populates="carpetas", passive_deletes=True)
    archivos = relationship(
        "File", back_populates="carpeta", passive_deletes=True)
