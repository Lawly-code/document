from httpx import AsyncClient

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_document_create(ac: AsyncClient, register_dto: RegisterDTO):
    resp_login = await ac.post(
        "/api/v1/custom",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        params={"description": "test description"},
    )

    assert resp_login.status_code == 201


async def test_document_create_with_not_token(ac: AsyncClient):
    resp_login = await ac.post(
        "/api/v1/custom", params={"description": "test description"}
    )

    assert resp_login.status_code == 403
