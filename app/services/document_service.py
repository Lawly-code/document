from datetime import datetime

from fastapi import Depends
from aiohttp import ClientSession
from lawly_db.db_models import DocumentCreation
from lawly_db.db_models.db_session import get_session
from lawly_db.db_models.enum_models import DocumentStatusEnum
from protos.ai_service.client import AIAssistantClient
from protos.ai_service.dto import AIRequestDTO
from protos.user_service.client import UserServiceClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse

from modules.documents import (
    DocumentCreateWithIdDTO,
    DocumentCreationResponseDTO,
    DocumentCreationUpdateWithUserIdDTO,
    DocumentDto,
    DocumentStructureDTO,
    ImprovedTextResponseDTO,
    GenerateDocumentDTO,
)
from modules.documents.dto import ImproveTextWithUserIDDTO
from modules.documents.enum import (
    DocumentUpdateEnum,
    ImproveTextEnum,
    GenerateDocumentEnum,
)
from repositories.document_creation_repository import DocumentCreationRepository
from repositories.document_repository import DocumentRepository
from repositories.s3_repository import S3Object
from repositories.template_repository import TemplateRepository
from utils.word_template_processor import WordTemplateProcessor


class DocumentService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.document_creation_repo = DocumentCreationRepository(session)
        self.document_repo = DocumentRepository(session)
        self.template_repo = TemplateRepository(session)

    async def create_document_service(
        self, document_create: DocumentCreateWithIdDTO
    ) -> DocumentCreationResponseDTO:
        """
        Создает новый шаблон документа
        :param document_create: DTO для создания документа
        :return: созданный шаблон
        """
        document = DocumentCreation(
            user_id=document_create.user_id,
            template_id=document_create.template_id,
            status=DocumentStatusEnum.STARTED,
            custom_name=document_create.custom_name,
        )
        await self.document_creation_repo.save(entity=document)
        return DocumentCreationResponseDTO.model_validate(
            document, from_attributes=True
        )

    async def update_document_service(
        self, document_creation_dto: DocumentCreationUpdateWithUserIdDTO
    ) -> DocumentCreationResponseDTO | DocumentUpdateEnum:
        """
        Обновляет статус создания документа
        :param document_creation_dto: DTO для обновления документа
        :return: обновленный шаблон
        """
        document = await self.document_creation_repo.get_document_creation_by_id(
            user_id=document_creation_dto.user_id,
            document_creation_id=document_creation_dto.document_creation_id,
        )
        if not document:
            return DocumentUpdateEnum.NOT_FOUND
        document.status = document_creation_dto.status
        document.error_message = document_creation_dto.error_message
        document.end_date = datetime.now()
        await self.document_creation_repo.save(entity=document)
        return DocumentCreationResponseDTO.model_validate(
            document, from_attributes=True
        )

    async def get_all_documents_service(self) -> list[DocumentDto]:
        """
        Получает все документы пользователя
        :param user_id: ID пользователя
        :return: список документов
        """
        documents = await self.document_repo.get_all_documents()
        return [
            DocumentDto.model_validate(document, from_attributes=True)
            for document in documents
        ]

    async def get_document_structure_service(
        self, document_id: int
    ) -> DocumentStructureDTO | None:
        """
        Получает структуру документа
        :param document_id: ID документа
        :return: структура документа
        """
        document = await self.document_repo.get_document_by_id(document_id=document_id)
        return (
            DocumentStructureDTO.model_validate(document, from_attributes=True)
            if document
            else None
        )

    async def improve_text_service(
        self, improve_text_dto: ImproveTextWithUserIDDTO
    ) -> ImprovedTextResponseDTO | ImproveTextEnum:
        """
        Улучшает текст документа
        :param improve_text_dto: DTO для улучшения текста
        :return: улучшенный текст
        """
        client_auth = UserServiceClient(host="user_grpc_service", port=50051)
        client_auth_info = await client_auth.get_user_info(
            user_id=improve_text_dto.user_id
        )
        if not client_auth_info.can_user_ai:
            return ImproveTextEnum.ACCESS_DENIED
        client = AIAssistantClient(host="ai_grpc_service", port=50051)
        improved_text = await client.improve_text(
            request_data=AIRequestDTO(user_prompt=improve_text_dto.text)
        )
        if not improved_text:
            return ImproveTextEnum.ERROR
        return ImprovedTextResponseDTO(improved_text=improved_text.assistant_reply)

    async def generate_document_service(
        self, generate_document_dto: GenerateDocumentDTO
    ) -> StreamingResponse | GenerateDocumentEnum:
        """
        Генерирует документ
        :param generate_document_dto: DTO для генерации документа
        :return:
        """
        try:
            template = await self.template_repo.get_template_by_id(
                template_id=generate_document_dto.template_id
            )
            if not template:
                return GenerateDocumentEnum.NOT_FOUND
            async with ClientSession() as session:
                async with session.get(template.download_url) as resp:
                    document_s3_obj = await resp.read()
            document_s3_obj = S3Object(
                body=document_s3_obj, content_type="application/octet-stream"
            )
            return await WordTemplateProcessor.fill_template(
                s3_object=document_s3_obj, fields=generate_document_dto.fields
            )
        except Exception:
            return GenerateDocumentEnum.ERROR
