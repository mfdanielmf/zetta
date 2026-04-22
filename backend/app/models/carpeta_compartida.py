import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.db import Base


class CarpetaCompartida(Base):
    __tablename__ = "carpetas_compartidas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_compartido = Column(DateTime, default=func.now())

    id_propietario = Column(UUID(as_uuid=True), ForeignKey(
        "usuarios.id"), nullable=False)
    id_receptor = Column(UUID(as_uuid=True), ForeignKey(
        "usuarios.id"), nullable=False)
    id_carpeta = Column(UUID(as_uuid=True), ForeignKey(
        "carpetas.id"), nullable=False)

    propietario = relationship(
        "User", back_populates="carpetas_compartidas", foreign_keys=[id_propietario], passive_deletes=True)
    receptor = relationship(
        "User", back_populates="carpetas_recibidas", foreign_keys=[id_receptor], passive_deletes=True)
    carpeta = relationship(
        "Folder", back_populates="compartida_con", passive_deletes=True)
