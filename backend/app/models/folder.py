import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.db import Base


class Folder(Base):
    __tablename__ = "carpetas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_original = Column(String(100), nullable=False)
    path = Column(String, nullable=False)
    favorito = Column(Boolean, default=False, nullable=False)
    fecha_favorito = Column(DateTime)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_eliminacion = Column(DateTime, nullable=True)

    id_usuario = Column(UUID(as_uuid=True), ForeignKey(
        "usuarios.id"), nullable=False)
    id_carpeta = Column(UUID(as_uuid=True), ForeignKey(
        "carpetas.id", ondelete="CASCADE"), nullable=True)

    carpeta = relationship("Folder",
                           remote_side=[id], back_populates="carpetas")
    usuario = relationship(
        "User", back_populates="carpetas", passive_deletes=True)
    archivos = relationship(
        "File", back_populates="carpeta", cascade="all, delete-orphan")
    carpetas = relationship(
        "Folder", back_populates="carpeta", cascade="all, delete-orphan")
    compartida_con = relationship(
        "CarpetaCompartida", back_populates="carpeta", passive_deletes=True)
