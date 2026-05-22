import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm  import relationship

from app.database.db import Base


class ArchivoFavorito(Base):
    __tablename__ = "archivos_favoritos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_favorito = Column(DateTime, default=func.now())

    id_usuario= Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    id_archivo = Column(UUID(as_uuid=True), ForeignKey("archivos.id", ondelete="CASCADE"), nullable=False)

    archivo = relationship("File", back_populates="favoritos", passive_deletes=True)