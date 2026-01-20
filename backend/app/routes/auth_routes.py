from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.user_schemas import UserCreate

auth_router = APIRouter()


@auth_router.post("/register")
async def register(usuario: UserCreate, db: Session = Depends(get_db)):
    return "test"
