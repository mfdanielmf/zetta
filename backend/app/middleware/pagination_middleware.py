from fastapi import Query

def get_pagination(pagina: int = Query(1, ge=1), limite: int = Query(25, ge=1, le=100)) -> tuple[int, int]:
    return pagina, limite