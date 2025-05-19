from httpx import AsyncClient
from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_custom_template_create(
    ac: AsyncClient, register_dto: RegisterDTO, patch_grpc_and_ai
):
    resp = await ac.post(
        "/api/v1/templates/custom",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={"description": "test description"},  # ✅ Должен совпадать с DTO
    )

    assert resp.status_code == 200
    assert (
        resp.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert resp.content
    assert resp.content.startswith(b"PK")


async def test_custom_template_create_with_not_token(
    ac: AsyncClient, patch_grpc_and_ai
):
    resp = await ac.post(
        "/api/v1/templates/custom",
        json={"description": "test description"},  # ✅ JSON тоже здесь
    )

    assert resp.status_code == 401
