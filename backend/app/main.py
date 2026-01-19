from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Health"])
async def root():
    return {"msg": "OK"}
