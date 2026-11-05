from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registra los modelos en Base.metadata)
from app.api.routes import clientes, facturas
from app.core.config import APP_NAME
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=APP_NAME, version="0.1.0", lifespan=lifespan)
app.include_router(clientes.router, prefix="/api/v1")
app.include_router(facturas.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
