from fastapi import Query


def get_filters(busqueda: str | None = Query(None, min_length=1, max_length=100)) -> str | None:
    return busqueda