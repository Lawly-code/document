from httpx import AsyncClient

from api.auth.auth_handler import sign_jwt
from dto import RegisterDTO


async def test_improve_text(
    ac: AsyncClient, register_dto: RegisterDTO, patch_grpc_and_ai
):
    response = await ac.post(
        "/api/v1/documents/improve-text",
        headers={"Authorization": f"Bearer {sign_jwt(user_id=register_dto.user.id)}"},
        json={"text": "Пример обычного текста, который нужно улучшить"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "improved_text" in data

    assert isinstance(data["improved_text"], str)

    assert "Пример обычного текста, который нужно улучшить" in data["improved_text"]

    assert data["improved_text"].startswith("Улучшено:")


async def test_improve_text_with_not_authorized(ac: AsyncClient):
    resp = await ac.post(
        "/api/v1/documents/improve-text",
        json={"text": "Пример обычного текста, который нужно улучшить"},
    )

    assert resp.status_code == 401
