import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.db import Base


class ArchivoCompartido(Base):
    __tablename__ = "archivos_compartidos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_compartido = Column(DateTime, default=func.now())

    id_propietario = Column(UUID(as_uuid=True), ForeignKey(
        "usuarios.id"), nullable=False)
    id_receptor = Column(UUID(as_uuid=True), ForeignKey(
        "usuarios.id"), nullable=False)
    id_archivo = Column(UUID(as_uuid=True), ForeignKey(
        "archivos.id", ondelete="CASCADE"), nullable=False)

    propietario = relationship(
        "User", back_populates="archivos_compartidos", foreign_keys=[id_propietario], passive_deletes=True)
    receptor = relationship(
        "User", back_populates="archivos_recibidos", foreign_keys=[id_receptor], passive_deletes=True)
    archivo = relationship(
        "File", back_populates="compartido_con", passive_deletes=True)
