import uuid
from app.database.db import Base
from sqlalchemy import UUID, Column, DateTime, String, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(20), nullable=False, unique=True)
    correo = Column(String(120), nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())

    archivos = relationship("File", back_populates="usuario", passive_deletes=True)
    carpetas = relationship("Folder", back_populates="usuario", passive_deletes=True)
