from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import StreamingResponse

from api.auth.auth_bearer import JWTHeader, JWTBearer
from modules.documents import (
    document_create_description,
    DocumentCreationResponseDTO,
    create_document_response,
    DocumentCreateDto,
    DocumentCreateWithIdDTO,
    document_update_description,
    update_document_response,
    DocumentCreationUpdateDTO,
    DocumentCreationUpdateWithUserIdDTO,
    get_documents_description,
    DocumentDto,
    get_documents_response,
    get_document_structure_description,
    DocumentStructureDTO,
    get_document_structure_response,
    ImprovedTextResponseDTO,
    improve_text_description,
    improve_text_response,
    ImproveTextDTO,
    GenerateDocumentDTO,
    generate_document_response,
)
from modules.documents.enum import DocumentUpdateEnum, ImproveTextEnum
from services.document_service import DocumentService

router = APIRouter(tags=["Документы"])


@router.post(
    "/create",
    summary="Начало процесса создания документа",
    description=document_create_description,
    response_model=DocumentCreationResponseDTO,
    responses=create_document_response,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(
    create_document_dto: DocumentCreateDto,
    document_service: DocumentService = Depends(DocumentService),
    token: JWTHeader = Depends(JWTBearer()),
):
    """
    Создает новый шаблон документа
    :param create_document_dto: DTO для создания документа
    :param document_service:
    :param token:
    :return:
    """
    result = await document_service.create_document_service(
        document_create=DocumentCreateWithIdDTO(
            user_id=token.user_id,
            template_id=create_document_dto.template_id,
            custom_name=create_document_dto.custom_name,
        )
    )
    return result


@router.put(
    "/update/{document_creation_id}",
    summary="Обновление статуса создания документа",
    description=document_update_description,
    response_model=DocumentCreationResponseDTO,
    responses=update_document_response,
    status_code=status.HTTP_200_OK,
)
async def update_document(
    document_creation_id: int,
    document_update_dto: DocumentCreationUpdateDTO,
    document_service: DocumentService = Depends(DocumentService),
    token: JWTHeader = Depends(JWTBearer()),
):
    """
    Обновляет статус создания документа
    :param document_creation_id: ID документа
    :param document_service:
    :param token:
    :return:
    """
    result = await document_service.update_document_service(
        document_creation_dto=DocumentCreationUpdateWithUserIdDTO(
            user_id=token.user_id,
            status=document_update_dto.status,
            error_message=document_update_dto.error_message,
            document_creation_id=document_creation_id,
        )
    )
    if result == DocumentUpdateEnum.NOT_FOUND:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Документ не найден у данного пользователя",
        )
    return result


@router.get(
    "/documents",
    summary="Получение списка базовых документов пользователя",
    description=get_documents_description,
    response_model=list[DocumentDto],
    status_code=status.HTTP_200_OK,
    responses=get_documents_response,
    dependencies=[Depends(JWTBearer())],
)
async def get_documents(document_service: DocumentService = Depends(DocumentService)):
    """
    Получение списка базовых документов пользователя
    :param document_service:
    :param token:
    :return:
    """
    result = await document_service.get_all_documents_service()
    return result


@router.get(
    "/document-structure/{document_id}",
    summary="Получение структуры документа",
    description=get_document_structure_description,
    response_model=DocumentStructureDTO,
    status_code=status.HTTP_200_OK,
    responses=get_document_structure_response,
    dependencies=[Depends(JWTBearer())],
)
async def get_document_structure(
    document_id: int,
    document_service: DocumentService = Depends(DocumentService),
):
    """
    Получение структуры документа
    :param document_id: ID документа
    :param document_service:
    :param token:
    :return:
    """
    result = await document_service.get_document_structure_service(
        document_id=document_id
    )
    if not result:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="Документ не найден"
        )
    return result


@router.post(
    "/improve-text",
    summary="Улучшение текста",
    description=improve_text_description,
    response_model=ImprovedTextResponseDTO,
    status_code=status.HTTP_200_OK,
    responses=improve_text_response,
    dependencies=[Depends(JWTBearer())],
)
async def improve_text(
    improve_text_dto: ImproveTextDTO,
    document_service: DocumentService = Depends(DocumentService),
):
    """
    Улучшение текста
    :param improve_text_dto: DTO для улучшения текста
    :param document_service:
    :param token:
    :return:
    """
    result = await document_service.improve_text_service(
        improve_text_dto=improve_text_dto
    )
    if result == ImproveTextEnum.ERROR:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Ошибка при улучшении текста",
        )
    return result


@router.post(
    "/generate",
    description="Генерация документа",
    response_class=StreamingResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_document_response,
    dependencies=[Depends(JWTBearer())],
)
async def generate_document(
    generate_document_dto: GenerateDocumentDTO,
    document_service: DocumentService = Depends(DocumentService),
):
    """
    Генерация документа
    :param generate_document_dto: DTO для генерации документа
    :param document_service:
    :param token:
    :return:
    """
    result = await document_service.generate_document_service(
        generate_document_dto=generate_document_dto
    )
    if result == ImproveTextEnum.ERROR:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Ошибка при генерации документа",
        )
    return result
