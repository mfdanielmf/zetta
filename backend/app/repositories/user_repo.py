from sqlalchemy.orm import Session
from app.models.user import User


def insert_user_db(usuario: User, db: Session) -> User:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def get_user_by_id(id: str, db: Session) -> User | None:
    usuario: User | None = db.get(User, id)

    return usuario


def get_user_by_name(nombre: str, db: Session) -> User | None:
    usuario: User | None = db.query(User).filter_by(nombre=nombre).first()

    return usuario


def get_user_by_email(correo: str, db: Session) -> User | None:
    usuario: User | None = db.query(User).filter_by(correo=correo).first()

    return usuario
