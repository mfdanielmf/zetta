from fastapi.middleware.cors import CORSMiddleware

from app.models.file import File
from app.models.user import User
from app.models.folder import Folder
from app.models.carpeta_compartida import CarpetaCompartida
from app.models.archivo_compartido import ArchivoCompartido

from app.routes.health_routes import health_router
from app.routes.auth_routes import auth_router
from app.routes.file_routes import file_router
from app.routes.folder_routes import folder_router
from app.routes.shared_routes import shared_router
from app.routes.item_routes import item_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.lifespan import lifespan
from app.core.logging_config import logger
from app.config import config

app = FastAPI(title="ZETTA", description="DOCS API ZETTA", lifespan=lifespan)

logger.info(f"Inicializando app. CONFIG: {config.ENVIRONMENT}")
logger.debug(f"CORS permitido: {config.ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"]
)

# RUTAS
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(file_router, prefix="/api/files", tags=["Files"])
app.include_router(folder_router, prefix="/api/folders", tags=["Folders"])
app.include_router(shared_router, prefix="/api/shared", tags=["Shared"])
app.include_router(item_router, prefix="/api/v2/items", tags=["Items"])
