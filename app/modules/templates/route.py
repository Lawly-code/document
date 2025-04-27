from fastapi import APIRouter, Depends, Query, Response, status

from modules.templates import get_templates_description, GetTemplatesResponseDTO, templates_response
from modules.templates.descriptions import get_template_info_description
from modules.templates.dto import GetTemplateDTO, TemplateInfoDto
from modules.templates.response import template_info_response
from services.template_service import TemplateService

router = APIRouter(tags=["Документы"])


@router.get(
    "/templates",
    summary="Получение доступных шаблонов",
    description=get_templates_description,
    response_model=GetTemplatesResponseDTO,
    responses=templates_response
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
        template_dto=GetTemplateDTO(query=query, limit=limit, offset=offset))
    return result


@router.get("templates/{template_id}",
            summary="Получение информации о шаблоне",
            description=get_template_info_description,
            response_model=TemplateInfoDto,
            responses=template_info_response)
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
            status_code=status.HTTP_404_NOT_FOUND, content="Шаблон не найден")
    return result
