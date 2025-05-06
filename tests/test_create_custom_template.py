from httpx import AsyncClient

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_custom_template_create(
    ac: AsyncClient, register_dto: RegisterDTO, patch_grpc_and_ai
):
    resp_login = await ac.post(
        "/api/v1/templates/custom",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        params={"description": "test description"},
    )

    assert resp_login.status_code == 200
    assert (
        resp_login.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert resp_login.content  # Проверяем, что не пустой файл пришел

    assert resp_login.content.startswith(b'PK')


async def test_custom_template_create_with_not_token(
    ac: AsyncClient, patch_grpc_and_ai
):
    resp_login = await ac.post(
        "/api/v1/templates/custom",
        params={"description": "test description"},
    )

    assert resp_login.status_code == 403
    assert resp_login.json() == {"detail": "Not authenticated"}
