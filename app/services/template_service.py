from fastapi import Depends
from lawly_db.db_models import Template
from lawly_db.db_models.db_session import get_session
from protos.ai_service.client import AIAssistantClient
from protos.ai_service.dto import AIRequestDTO
from protos.user_service.client import UserServiceClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from modules.templates import (
    GetTemplateDTO,
    GetTemplatesResponseDTO,
    TemplateDTO,
    TemplateInfoDto,
    DocumentDto,
    FieldDTO,
    CreateTemplateDTO,
)
from modules.templates.dto import TemplateDownloadDTO
from modules.templates.enum import CreateCustomTemplateEnum
from repositories.template_repository import TemplateRepository
from utils.word_template_processor import WordTemplateProcessor


class TemplateService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.template_repo = TemplateRepository(session)

    async def get_templates_service(
        self, template_dto: GetTemplateDTO
    ) -> GetTemplatesResponseDTO:
        """
        Получение списка шаблонов документов
        :param template_dto: DTO для получения шаблонов
        :return: Список шаблонов
        """
        templates = await self.template_repo.get_templates(
            query=template_dto.query,
            limit=template_dto.limit,
            offset=template_dto.offset,
        )
        total = await self.template_repo.get_total_documents(query=template_dto.query)
        return GetTemplatesResponseDTO(
            total=total,
            templates=[
                TemplateDTO.model_validate(template, from_attributes=True)
                for template in templates
            ],
        )

    async def get_template_info_service(
        self, template_id: int
    ) -> TemplateInfoDto | None:
        """
        Получение информации о шаблоне документа
        :param template_id: ID шаблона
        :return: Информация о шаблоне
        """
        template = await self.template_repo.get_template_by_id(template_id)
        if not template:
            return None
        documents = {}
        custom_fields = []
        template_fields = template.fields

        for field in template_fields:
            print(field.id)
            if field.document:
                await self.session.refresh(
                    field.document, attribute_names=["fields"]
                )  # 👈 прогружаем связи
                doc_dto = DocumentDto.model_validate(
                    field.document, from_attributes=True
                )
                documents[doc_dto.id] = doc_dto  # Убираем дубли по ID
            else:
                custom_fields.append(
                    FieldDTO.model_validate(field, from_attributes=True)
                )

        return TemplateInfoDto(
            required_documents=list(documents.values()),
            custom_fields=custom_fields,
            id=template.id,
            name=template.name,
            name_ru=template.name_ru,
            description=template.description,
            image_url=template.image_url,
            download_url=template.download_url,
        )

    async def get_template_download_url_service(
        self, template_id: int
    ) -> TemplateDownloadDTO | None:
        """
        Получение ссылки на скачивание шаблона
        :param template_id: ID шаблона
        :return: Ссылка на скачивание шаблона
        """
        template = await self.template_repo.get_template_by_id(template_id)
        if template is None:
            return None
        return TemplateDownloadDTO(download_url=template.download_url)

    async def create_custom_template_service(
        self, create_template_dto: CreateTemplateDTO
    ) -> StreamingResponse | CreateCustomTemplateEnum:
        """
        Создание кастомного шаблона
        :param create_template_dto: DTO для создания кастомного шаблона
        :return: Информация о созданном шаблоне
        """
        client_auth = UserServiceClient(host="user_grpc_service", port=50051)
        client_auth_info = await client_auth.get_user_info(
            user_id=create_template_dto.user_id
        )
        if (
            not client_auth_info.can_create_custom_templates
            or not client_auth_info.can_user_ai
        ):
            return CreateCustomTemplateEnum.ACCESS_DENIED
        client = AIAssistantClient(host="ai_grpc_service", port=50051)
        ai_description = await client.custom_template(
            request_data=AIRequestDTO(user_prompt=create_template_dto.description)
        )
        if not ai_description:
            return CreateCustomTemplateEnum.ERROR
        name_ru = "Тестовый шаблон"
        generate_template = Template(
            user_id=create_template_dto.user_id,
            name="Test template",
            name_ru="Тестовый шаблон",
            description="Тестовое описание шаблона",
            image_url="https://example.com/image.png",
            download_url="https://example.com/download.zip",
        )
        await self.template_repo.create(entity=generate_template)

        filename = name_ru + ".docx"

        return await WordTemplateProcessor.generate_docx_response(
            text=ai_description.assistant_reply, filename=filename
        )
