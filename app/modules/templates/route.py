from fastapi import APIRouter, status, Query, Depends, Response, Path

from api.auth.auth_bearer import JWTHeader, JWTBearer
from modules.templates import (
    get_templates_description,
    GetTemplatesResponseDTO,
    templates_response,
    GetTemplateDTO,
    get_template_info_description,
    TemplateInfoDto,
    template_info_response,
    download_template_description,
    custom_template_description,
    CustomTemplateDTO,
    custom_template_response,
    CreateTemplateDTO,
)
from services.template_service import TemplateService

router = APIRouter(tags=["Шаблоны"])


@router.get(
    "/templates",
    summary="Получение доступных шаблонов",
    description=get_templates_description,
    response_model=GetTemplatesResponseDTO,
    responses=templates_response,
    status_code=status.HTTP_200_OK,
)
async def get_templates(
    query: str | None = Query(None, description="Поисковый запрос"),
    limit: int = Query(20, ge=1, description="Максимум результатов (по умолчанию 20)"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    template_service: TemplateService = Depends(TemplateService),
):
    """
    Получение доступных шаблонов
    :return: Список доступных шаблонов
    """
    result = await template_service.get_templates_service(
        template_dto=GetTemplateDTO(query=query, limit=limit, offset=offset)
    )
    return result


@router.get(
    "/templates/{template_id}",
    summary="Получение информации о шаблоне",
    description=get_template_info_description,
    response_model=TemplateInfoDto,
    responses=template_info_response,
    status_code=status.HTTP_200_OK,
)
async def get_template_info(
    template_id: int,
    template_service: TemplateService = Depends(TemplateService),
):
    """
    Получение информации о шаблоне
    :param template_id: ID шаблона
    :return: Информация о шаблоне
    """
    result = await template_service.get_template_info_service(template_id=template_id)
    if result is None:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Шаблон не найден"
        )
    return result


@router.get(
    "/templates/{template_id}/download",
    summary="Получение ссылки на скачивание шаблона",
    description=download_template_description,
    response_model=str,
    responses=template_info_response,
    status_code=status.HTTP_200_OK,
)
async def download_template(
    template_id: int = Path(..., description="Идентификатор шаблона для загрузки"),
    template_service: TemplateService = Depends(TemplateService),
):
    """
    Получение ссылки на скачивание шаблона
    :param template_id: ID шаблона
    :return: Ссылка на скачивание шаблона
    """
    result = await template_service.get_template_download_url_service(
        template_id=template_id
    )
    if not result:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Шаблон не найден"
        )

    return result


@router.post(
    "/custom",
    summary="Создание кастомного шаблона",
    description=custom_template_description,
    response_model=CustomTemplateDTO,
    responses=custom_template_response,
    status_code=status.HTTP_201_CREATED,
)
async def create_custom_template(
    description: str | None = Query(None, description="Описание шаблона"),
    template_service: TemplateService = Depends(TemplateService),
    token: JWTHeader = Depends(JWTBearer()),
):
    """
    Создание кастомного шаблона
    :param create_template_dto: DTO для создания кастомного шаблона
    :return: Информация о кастомном шаблоне
    """

    result = await template_service.create_custom_template_service(
        create_template_dto=CreateTemplateDTO(
            user_id=token.user_id, description=description
        )
    )
    if not result:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Ошибка создания кастомного шаблона",
        )
    return result
