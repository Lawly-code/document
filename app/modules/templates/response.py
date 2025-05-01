from modules.templates import GetTemplatesResponseDTO
from modules.templates.dto import TemplateInfoDto, CustomTemplateDTO
from shared import base_response

templates_response = {
    **base_response,
    200: {
        "description": "Список шаблонов документов",
        "model": GetTemplatesResponseDTO,
    },
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

download_template_response = {
    **base_response,
    200: {
        "description": "Ссылка на скачивание шаблона",
        "model": str,
    },
    404: {
        "description": "Шаблон не найден",
    },
}

custom_template_response = {
    **base_response,
    201: {
        "description": "Шаблон успешно создан",
        "model": CustomTemplateDTO,
    },
    400: {
        "description": "Ошибка создания кастомного шаблона",
    },
    403: {"description": "Нет доступа к ресурсу"},
}
