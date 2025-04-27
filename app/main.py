from contextlib import asynccontextmanager

from dotenv import load_dotenv

from api import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lawly_db.db_models.db_session import global_init

load_dotenv("./.env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await global_init()  # 👈 здесь всё что ты делал в startup
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
