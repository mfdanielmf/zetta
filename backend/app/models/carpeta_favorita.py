import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database.db import Base


class CarpetaFavorita(Base):
    __tablename__ = "carpetas_favoritas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_favorito = Column(DateTime, default=func.now())

    id_usuario= Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    id_carpeta = Column(UUID(as_uuid=True), ForeignKey("carpetas.id", ondelete="CASCADE"), nullable=False)

    carpeta = relationship("Folder", back_populates="favoritos", passive_deletes=True)