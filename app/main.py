from contextlib import asynccontextmanager

from api import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lawly_db.db_models.db_session import global_init


@asynccontextmanager
async def lifespan(app: FastAPI):
    await global_init()
    yield


app = FastAPI(title="Lawly User API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
