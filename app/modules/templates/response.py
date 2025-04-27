from modules.templates import GetTemplatesResponseDTO
from modules.templates.dto import TemplateInfoDto
from shared import base_response

templates_response = {
    **base_response,
    200: {
        "description": "Список шаблонов документов",
        "model": GetTemplatesResponseDTO,
    }
}

template_info_response = {
    **base_response,
    200: {
        "description": "Информация о шаблоне",
        "model": TemplateInfoDto,
    },
    404: {
        "description": "Шаблон не найден",
    },
}
