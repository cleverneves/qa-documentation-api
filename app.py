from fastapi import FastAPI
from api.routes.ask import router as ask_router

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(ask_router)
