from .descriptions import (
    document_create_description,
    document_update_description,
    get_documents_description,
    get_document_structure_description,
    improve_text_description,
)
from .dto import (
    TemplateDTO,
    DocumentCreateDto,
    DocumentCreateWithIdDTO,
    DocumentCreationResponseDTO,
    DocumentCreationUpdateDTO,
    DocumentCreationUpdateWithUserIdDTO,
    DocumentDto,
    FieldDTO,
    DocumentStructureDTO,
    ImproveTextDTO,
    ImprovedTextResponseDTO,
    GenerateDocumentDTO,
)

from .response import (
    create_document_response,
    update_document_response,
    get_documents_response,
    get_document_structure_response,
    improve_text_response,
    generate_document_response,
)
from .route import router

__all__ = [
    "router",
    "document_create_description",
    "document_update_description",
    "get_documents_description",
    "get_document_structure_description",
    "improve_text_description",
    "DocumentCreateDto",
    "DocumentCreateWithIdDTO",
    "DocumentCreationResponseDTO",
    "DocumentCreationUpdateDTO",
    "DocumentCreationUpdateWithUserIdDTO",
    "DocumentDto",
    "FieldDTO",
    "TemplateDTO",
    "DocumentStructureDTO",
    "ImproveTextDTO",
    "ImprovedTextResponseDTO",
    "create_document_response",
    "update_document_response",
    "get_documents_response",
    "get_document_structure_response",
    "improve_text_response",
    "GenerateDocumentDTO",
    "generate_document_response",
]
