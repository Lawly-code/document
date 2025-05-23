from modules.documents import DocumentStructureDTO
from modules.documents.dto import (
    DocumentCreationResponseDTO,
    DocumentDto,
    ImprovedTextResponseDTO,
)
from shared import base_response

create_document_response = {
    **base_response,
    201: {
        "description": "Документ успешно создан",
        "model": DocumentCreationResponseDTO,
    },
    401: {
        "description": "Нет доступа к ресурсу",
    },
}

update_document_response = {
    **base_response,
    200: {
        "description": "Документ успешно обновлен",
        "model": DocumentCreationResponseDTO,
    },
    404: {
        "description": "Документ не найден у данного пользователя",
    },
    401: {"description": "Нет доступа к ресурсу"},
}

get_documents_response = {
    **base_response,
    200: {
        "description": "Список документов",
        "model": list[DocumentDto],
    },
    401: {"description": "Нет доступа к ресурсу"},
}
get_document_structure_response = {
    **base_response,
    200: {
        "description": "Структура документа",
        "model": DocumentStructureDTO,
    },
    404: {
        "description": "Документ не найден",
    },
    401: {"description": "Нет доступа к ресурсу"},
}

improve_text_response = {
    **base_response,
    200: {
        "description": "Текст успешно преобразован",
        "model": ImprovedTextResponseDTO,
    },
    400: {
        "description": "Ошибка при улучшении текста",
    },
    401: {"description": "Нет доступа к ресурсу"},
    403: {"description": "Недостаточно прав для выполнения"},
}

generate_document_response = {
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
        "description": "Ошибка при создании документа",
    },
    401: {"description": "Нет доступа к ресурсу"},
    403: {"description": "Недостаточно прав для выполнения"},
}
