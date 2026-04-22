import uuid
from app.database.db import Base
from sqlalchemy import UUID, Column, DateTime, String, func
from sqlalchemy.orm import relationship

from app.models.carpeta_compartida import CarpetaCompartida


class User(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(20), nullable=False, unique=True)
    correo = Column(String(120), nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())

    archivos = relationship(
        "File", back_populates="usuario", passive_deletes=True)
    carpetas = relationship(
        "Folder", back_populates="usuario", passive_deletes=True)
    carpetas_compartidas = relationship(
        "CarpetaCompartida", back_populates="propietario", foreign_keys=[CarpetaCompartida.id_propietario], passive_deletes=True)
    carpetas_recibidas = relationship(
        "CarpetaCompartida", back_populates="receptor", foreign_keys=[CarpetaCompartida.id_receptor], passive_deletes=True)
