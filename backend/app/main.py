from app.models.file import File
from app.models.user import User
from app.routes.health_routes import health_router
from app.routes.auth_routes import auth_router
from app.routes.file_routes import file_router
from fastapi import FastAPI

app = FastAPI(title="ZETTA", description="DOCS API ZETTA")

# MODELOS DB

# RUTAS
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(file_router, prefix="/api/files", tags=["Files"])
