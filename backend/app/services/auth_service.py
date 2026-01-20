from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate


def crear_usuario(db: Session, usuario: UserCreate):
    pass
