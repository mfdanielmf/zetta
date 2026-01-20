from app.routes.health_routes import health_router
from app.routes.auth_routes import auth_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
