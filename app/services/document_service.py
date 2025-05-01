from datetime import datetime

from fastapi import Depends
from lawly_db.db_models import DocumentCreation
from lawly_db.db_models.db_session import get_session
from lawly_db.db_models.enum_models import DocumentStatusEnum
from sqlalchemy.ext.asyncio import AsyncSession

from modules.documents import (
    DocumentCreateWithIdDTO,
    DocumentCreationResponseDTO,
    DocumentCreationUpdateWithUserIdDTO,
    DocumentUpdateEnum,
    DocumentDto,
    DocumentStructureDTO,
    ImproveTextDTO,
    ImprovedTextResponseDTO,
    ImproveTextEnum,
)
from repositories.document_creation_repository import DocumentCreationRepository
from repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.document_creation_repo = DocumentCreationRepository(session)
        self.document_repo = DocumentRepository(session)

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
        self, improve_text_dto: ImproveTextDTO
    ) -> ImprovedTextResponseDTO | ImproveTextEnum:
        """
        Улучшает текст документа
        :param improve_text_dto: DTO для улучшения текста
        :return: улучшенный текст
        """
        try:
            # Здесь должна быть логика улучшения текста
            improved_text = improve_text_dto.text + " улучшили"
            return ImprovedTextResponseDTO(improved_text=improved_text)
        except Exception as e:
            print(f"Error improving text: {e}")
            return ImproveTextEnum.ERROR
