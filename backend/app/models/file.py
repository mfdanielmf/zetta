import uuid
from sqlalchemy import Column, UUID, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database.db import Base


class File(Base):
    __tablename__ = "archivos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_original = Column(String(100), nullable=False)
    path = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())
    id_usuario = Column(Integer, ForeignKey("user.id"), nullable=False)

    usuario = relationship(
        "User", back_populates="archivos", passive_deletes=True)
