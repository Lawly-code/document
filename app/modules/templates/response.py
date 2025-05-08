from modules.templates import GetTemplatesResponseDTO
from modules.templates.dto import (
    TemplateInfoDto,
    TemplateDownloadDTO,
)
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
        "model": TemplateDownloadDTO,
    },
    404: {
        "description": "Шаблон не найден",
    },
}

custom_template_response = {
    **base_response,
    200: {
        "description": "Документ успешно создан",
        "content": {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
                "schema": {"type": "string", "format": "binary"}
            }
        },
    },
    400: {
        "description": "Ошибка создания кастомного шаблона",
    },
    401: {"description": "Нет доступа к ресурсу"},
    403: {"description": "Недостаточно прав для выполнения"},
}

download_empty_template = {
    **base_response,
    200: {
        "description": "Шаблон успешно скачан",
        "content": {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
                "schema": {"type": "string", "format": "binary"}
            }
        },
    },
    400: {
        "description": "Ошибка скачивания шаблона",
    },
    401: {"description": "Нет доступа к ресурсу"},
    404: {"description": "Шаблон не найден"},
}
