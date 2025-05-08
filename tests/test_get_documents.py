import logging

from httpx import AsyncClient
from lawly_db.db_models import Document
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO

logging.basicConfig(level=logging.INFO)
__log__ = logging.getLogger(__name__)


async def test_get_documents(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    __log__.info("тест получения документов")
    document = Document(
        name="test_document",
        name_ru="тестовые документы",
        link="https://test_link",
        description="тестовое описание",
    )
    session.add(document)
    await session.commit()

    resp = await ac.get(
        "/api/v1/documents/documents",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
    )
    __log__.info("результат запроса")
    __log__.info(f"Response: {resp.json()}")
    await session.delete(document)
    await session.commit()

    assert resp.status_code == 200

    data = resp.json()

    assert isinstance(data, list)
    assert len(data) > 0

    doc = data[0]
    assert "id" in doc
    assert "name" in doc
    assert "name_ru" in doc
    assert "link" in doc
    assert "description" in doc

    assert isinstance(doc["id"], int)
    assert isinstance(doc["name"], str)
    assert isinstance(doc["name_ru"], str)
    assert isinstance(doc["link"], str)
    assert isinstance(doc["description"], str)


async def test_get_documents_with_not_authorized(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    document = Document(
        name="test_document",
        name_ru="тестовые документы",
        link="https://test_link",
        description="тестовое описание",
    )
    session.add(document)
    await session.commit()

    resp = await ac.get(
        "/api/v1/documents/documents",
    )
    await session.delete(document)
    await session.commit()

    assert resp.status_code == 401


async def test_get_document_structure_by_id_not_authorized(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    document = Document(
        name="test_document",
        name_ru="тестовые документы",
        link="https://test_link",
        description="тестовое описание",
    )
    session.add(document)
    await session.commit()

    resp = await ac.get(
        "/api/v1/documents/documents", params={"document_id": document.id}
    )
    await session.delete(document)
    await session.commit()
    assert resp.status_code == 401


async def test_get_document_structure_by_id_not_found_document(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    resp = await ac.get(
        "/api/v1/documents/documents-structure",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        params={"document_id": 99999},
    )

    assert resp.status_code == 404


async def test_get_document_structure_by_id(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    document = Document(
        name="test_document",
        name_ru="тестовые документы",
        link="https://test_link",
        description="тестовое описание",
    )
    session.add(document)
    await session.commit()

    resp = await ac.get(
        f"/api/v1/documents/document-structure/{document.id}",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
    )

    await session.delete(document)
    await session.commit()

    assert resp.status_code == 200

    data = resp.json()

    assert isinstance(data, dict)

    assert "id" in data
    assert "name" in data
    assert "name_ru" in data
    assert "link" in data
    assert "description" in data

    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["name_ru"], str)
    assert isinstance(data["link"], str)
    assert isinstance(data["description"], str)

    assert data["id"] == document.id
    assert data["name"] == "test_document"
    assert data["name_ru"] == "тестовые документы"
    assert data["link"] == "https://test_link"
    assert data["description"] == "тестовое описание"
