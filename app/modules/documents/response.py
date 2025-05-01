from modules.documents.dto import DocumentCreationResponseDTO, DocumentDto
from shared import base_response

create_document_response = {
    **base_response,
    201: {
        "description": "Документ успешно создан",
        "model": DocumentCreationResponseDTO,
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
}

get_documents_response = {
    **base_response,
    200: {
        "description": "Список документов",
        "model": list[DocumentDto],
    },
}
get_document_structure_response = {
    **base_response,
    200: {
        "description": "Структура документа",
        "model": DocumentDto,
    },
    404: {
        "description": "Документ не найден",
    },
}

improve_text_response = {
    **base_response,
    200: {
        "description": "Текст успешно преобразован",
        "model": DocumentDto,
    },
    400: {
        "description": "Ошибка при улучшении текста",
    },
}
