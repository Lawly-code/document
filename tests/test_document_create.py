from httpx import AsyncClient
from lawly_db.db_models import Template
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_document_create(
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
    resp = await ac.post(
        "/api/v1/documents/create",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={"template_id": template.id, "custom_name": "тестовое имя"},
    )
    await session.delete(template)
    assert resp.status_code == 201
