
import logging
import sys
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "app.log"


def config_logging():
    logger = logging.getLogger("ZETTA")

    if logger.handlers:
        return logger

    log_level = logging.INFO

    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(log_format)
    logger.addHandler(stdout_handler)

    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as ex:
        logger.warning(f"No se pudo crear archivo de log: {ex}")

    logger.setLevel(log_level)
    logger.propagate = False

    return logger


logger = config_logging()
