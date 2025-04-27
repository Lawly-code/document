import string
import uuid
from datetime import datetime, UTC, timedelta
from typing import AsyncGenerator
from os import getenv as env

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from lawly_db.db_models import User, RefreshSession
from lawly_db.db_models.db_session import get_session, Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

import random

from app.repositories.cipher_repository import CipherRepository
from app.main import app

import time

from config import settings
from dto import RegisterDTO

time.sleep(2)

# DATABASE
DATABASE_URL_TEST = (
    f'postgresql+asyncpg://{env("test_db_login")}:{env("test_db_password")}'
    f'@{env("test_db_host")}:{env("test_db_port")}/{env("test_db_name")}'
)

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)

async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)

Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


# # SETUP
# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


