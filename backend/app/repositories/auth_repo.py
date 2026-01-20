from sqlalchemy.orm import Session
from app.models.user import User


def crear_usuario(db: Session, usuario: User) -> User:
    db.add(usuario)
    db.commit()
    db.flush(usuario)

    return usuario
