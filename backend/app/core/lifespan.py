from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.scheduler import scheduler
from app.services.trash_services import eliminar_data_papelera
from app.database.db import SessionLocal
from apscheduler.triggers.interval import IntervalTrigger


def limpiar_papelera():
    db = SessionLocal()

    try:
        eliminar_data_papelera(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Zetta: Aplicación iniciada. Limpiando papelera", flush=True)

    limpiar_papelera()

    scheduler.add_job(limpiar_papelera, IntervalTrigger(
        hours=12), id="job_limpieza_papelera", replace_existing=True, max_instances=1, coalesce=True)

    scheduler.start()

    print("Zetta: Papelera limpiada. Scheduler iniciado", flush=True)

    yield

    print("Zetta: Parando scheduler papelera", flush=True)
    scheduler.shutdown()
