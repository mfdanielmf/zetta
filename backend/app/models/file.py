import uuid
from sqlalchemy import Boolean, Column, UUID, ForeignKey, String, DateTime, func, BigInteger
from sqlalchemy.orm import relationship
from app.database.db import Base


class File(Base):
    __tablename__ = "archivos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_original = Column(String(100), nullable=False)
    path = Column(String, nullable=False)
    tamaño_bytes = Column(BigInteger, nullable=False)
    favorito = Column(Boolean, default=False, nullable=False)
    fecha_favorito = Column(DateTime, default=func.now())
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_eliminacion = Column(DateTime, nullable=True)

    id_usuario = Column(UUID(as_uuid=True), ForeignKey(
        "usuarios.id"), nullable=False)
    id_carpeta = Column(UUID(as_uuid=True), ForeignKey(
        "carpetas.id"), nullable=True)

    usuario = relationship(
        "User", back_populates="archivos", passive_deletes=True)
    carpeta = relationship(
        "Folder", back_populates="archivos", passive_deletes=True)
    compartido_con = relationship(
        "ArchivoCompartido", back_populates="archivo", passive_deletes=True)
