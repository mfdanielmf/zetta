from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.scheduler import scheduler
from app.core.logging_config import logger
from app.services.trash_services import eliminar_data_papelera
from app.database.db import SessionLocal
from apscheduler.triggers.interval import IntervalTrigger

def limpiar_papelera():
    db = SessionLocal()

    try:
        logger.info("Limpiando papelera...")
        eliminar_data_papelera(db)
        logger.info("Papelera limpiada correctamente")
    except Exception as ex:
        logger.error(f"Error al limpiar papelera: {ex}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicializando ZETTA")

    limpiar_papelera()

    scheduler.add_job(limpiar_papelera, IntervalTrigger(
        hours=12), id="job_limpieza_papelera", replace_existing=True, max_instances=1, coalesce=True)

    scheduler.start()
    logger.info("Scheduler iniciado. Tareas programadas activas")

    yield

    logger.info("Deteniendo ZETTA")
    scheduler.shutdown()
    logger.info("Aplicación detenida correctamente")
