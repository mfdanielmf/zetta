from fastapi import Query


def get_filters(busqueda: str | None = Query(None, max_length=100)) -> str | None:
    return busqueda.strip() if busqueda and len(busqueda) > 0 else None