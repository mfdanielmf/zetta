from fastapi import APIRouter

h_router = APIRouter(tags=["Health"])


@h_router.get("/")
def health():
    return {"msg": "OK"}
