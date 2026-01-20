import datetime
import uuid
from app.database.db import Base
from sqlalchemy import UUID, Column, DateTime, String


class User(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(20), nullable=False, unique=True)
    correo = Column(String(120), nullable=False, unique=True)
    contraseña = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.UTC)
