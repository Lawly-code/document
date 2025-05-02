from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from lawly_db.db_models import Template


async def test_get_templates(ac: AsyncClient, session: AsyncSession):
    template1 = Template(
        name="test_template",
        name_ru="тестовый шаблон",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )
    template2 = Template(
        name="test_template",
        name_ru="документ",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )

    session.add(template1)
    session.add(template2)
    await session.commit()

    resp = await ac.get("/api/v1/templates", params={"query": "тестовы"})

    assert resp.status_code == 200

    data = resp.json()

    assert data["total"] == 1

    response_templates = [
        {
            "name": template["name"],
            "name_ru": template["name_ru"],
            "description": template["description"],
            "image_url": template["image_url"],
            "download_url": template["download_url"],
        }
        for template in data["templates"]
    ]

    expected_templates_simplified = [
        {
            "name": "test_template",
            "name_ru": "тестовый шаблон",
            "description": "тестовое описание",
            "image_url": "https://image_url",
            "download_url": "https://test_download_url",
        }
    ]

    assert response_templates == expected_templates_simplified

    await session.delete(template1)
    await session.delete(template2)
    await session.commit()


async def test_get_templates_with_empty_query(ac: AsyncClient, session: AsyncSession):
    template1 = Template(
        name="test_template",
        name_ru="тестовый шаблон",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )
    template2 = Template(
        name="test_template",
        name_ru="документ",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )

    session.add(template1)
    session.add(template2)
    await session.commit()

    resp = await ac.get("/api/v1/templates", params={"query": ""})

    assert resp.status_code == 200

    data = resp.json()

    assert data["total"] == 2

    response_templates = [
        {
            "name": template["name"],
            "name_ru": template["name_ru"],
            "description": template["description"],
            "image_url": template["image_url"],
            "download_url": template["download_url"],
        }
        for template in data["templates"]
    ]

    expected_templates_simplified = [
        {
            "name": "test_template",
            "name_ru": "тестовый шаблон",
            "description": "тестовое описание",
            "image_url": "https://image_url",
            "download_url": "https://test_download_url",
        },
        {
            "name": "test_template",
            "name_ru": "документ",
            "description": "тестовое описание",
            "image_url": "https://image_url",
            "download_url": "https://test_download_url",
        },
    ]

    assert sorted(response_templates, key=lambda x: x["name_ru"]) == sorted(
        expected_templates_simplified, key=lambda x: x["name_ru"]
    )

    await session.delete(template1)
    await session.delete(template2)
    await session.commit()


async def test_get_template_detail(ac: AsyncClient, session: AsyncSession):
    template = Template(
        name="test_template",
        name_ru="тестовый шаблон",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )

    session.add(template)
    await session.commit()
    resp = await ac.get(f"/api/v1/templates/{template.id}")

    assert resp.status_code == 200

    data = resp.json()

    assert data["id"] == template.id
    assert data["name"] == "test_template"
    assert data["name_ru"] == "тестовый шаблон"
    assert data["description"] == "тестовое описание"
    assert data["image_url"] == "https://image_url"
    assert data["download_url"] == "https://test_download_url"

    assert isinstance(data["required_documents"], list)
    assert isinstance(data["custom_fields"], list)

    await session.delete(template)
    await session.commit()


async def test_get_template_detail_not_found(ac: AsyncClient, session: AsyncSession):
    non_existent_id = 99999

    resp = await ac.get(f"/api/v1/templates/{non_existent_id}")

    assert resp.status_code == 404


async def test_download_template_success(ac: AsyncClient, session: AsyncSession):
    template = Template(
        name="test_template",
        name_ru="тестовый шаблон",
        description="тестовое описание",
        image_url="https://image_url",
        download_url="https://test_download_url",
    )

    session.add(template)
    await session.commit()

    resp = await ac.get(f"/api/v1/templates/{template.id}/download")

    assert resp.status_code == 200

    download_url = resp.json()
    assert "download_url" in download_url
    assert download_url["download_url"] == "https://test_download_url"

    await session.delete(template)
    await session.commit()


async def test_download_template_not_found(ac: AsyncClient, session: AsyncSession):
    non_existent_id = 99999

    resp = await ac.get(f"/api/v1/templates/{non_existent_id}/download")

    assert resp.status_code == 404
