from httpx import AsyncClient
from lawly_db.db_models import DocumentCreation, Template
from lawly_db.db_models.enum_models import DocumentStatusEnum
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_update_document_creation_status(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    template = Template(
        name="test_template",
        name_ru="тестовый шаблон",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )
    session.add(template)
    await session.commit()

    document = DocumentCreation(
        user_id=register_dto.user.id,
        template_id=template.id,
        status=DocumentStatusEnum.STARTED,
        custom_name="тестовое кастомное имя",
    )
    session.add(document)
    await session.commit()

    resp = await ac.put(
        f"/api/v1/documents/update/{document.id}",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={"status": "completed"},
    )

    await session.delete(document)
    await session.delete(template)

    assert resp.status_code == 200
    data = resp.json()

    assert data["id"] == document.id
    assert data["status"] == "completed"
    assert data["error_message"] is None
    assert data["custom_name"] == "тестовое кастомное имя"
    assert data["user_id"] == register_dto.user.id
    assert data["template_id"] == template.id


async def test_update_document_creation_not_authorized(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    template = Template(
        name="test_template",
        name_ru="тестовый шаблон",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )
    session.add(template)
    await session.commit()

    document = DocumentCreation(
        user_id=register_dto.user.id,
        template_id=template.id,
        status=DocumentStatusEnum.STARTED,
        custom_name="тестовое кастомное имя",
    )
    session.add(document)
    await session.commit()

    resp = await ac.put(
        f"/api/v1/documents/update/{document.id}", json={"status": "completed"}
    )

    await session.delete(document)
    await session.delete(template)
    await session.commit()
    assert resp.status_code == 401


async def test_update_document_creation_status_404_not_found(
    ac: AsyncClient, register_dto: RegisterDTO
):
    non_existing_document_id = 999999

    resp = await ac.put(
        f"/api/v1/documents/update/{non_existing_document_id}",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={"status": "completed"},
    )

    assert resp.status_code == 404


async def test_update_document_creation_status_422_validation_error(
    ac: AsyncClient, session: AsyncSession, register_dto: RegisterDTO
):
    template = Template(
        name="test_template",
        name_ru="тестовый шаблон",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )
    session.add(template)
    await session.commit()

    document = DocumentCreation(
        user_id=register_dto.user.id,
        template_id=template.id,
        status=DocumentStatusEnum.STARTED,
        custom_name="тестовое кастомное имя",
    )
    session.add(document)
    await session.commit()

    resp = await ac.put(
        f"/api/v1/documents/update/{document.id}",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={"status": "INVALID_STATUS"},
    )
    await session.delete(document)
    await session.delete(template)
    await session.commit()

    assert resp.status_code == 422
