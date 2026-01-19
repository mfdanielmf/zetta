from app.routes.health import h_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(h_router)
