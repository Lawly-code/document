from fastapi import Depends
from lawly_db.db_models.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from modules.templates.dto import GetTemplateDTO, GetTemplatesResponseDTO, TemplateDTO, TemplateInfoDto, DocumentDto, \
    FieldDTO
from repositories.template_repository import TemplateRepository


class TemplateService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.template_repo = TemplateRepository(session)

    async def get_templates_service(self, template_dto: GetTemplateDTO) -> GetTemplatesResponseDTO:
        """
        Получение списка шаблонов документов
        :param template_dto: DTO для получения шаблонов
        :return: Список шаблонов
        """
        templates = await self.template_repo.get_templates(
            query=template_dto.query,
            limit=template_dto.limit,
            offset=template_dto.offset
        )
        total = await self.template_repo.get_total_documents(
            query=template_dto.query
        )
        return GetTemplatesResponseDTO(total=total,
                                       templates=[TemplateDTO.model_validate(template, from_attributes=True) for
                                                  template in
                                                  templates])

    async def get_template_info_service(self, template_id: int) -> TemplateInfoDto | None:
        """
        Получение информации о шаблоне документа
        :param template_id: ID шаблона
        :return: Информация о шаблоне
        """
        template = await self.template_repo.get_template_by_id(template_id)
        print("получаем шаблон")
        documents = {}
        custom_fields = []
        template_fields = template.fields

        for field in template_fields:
            print(field.id)
            if field.document:
                await self.session.refresh(field.document, attribute_names=["fields"])  # 👈 прогружаем связи
                doc_dto = DocumentDto.model_validate(field.document, from_attributes=True)
                documents[doc_dto.id] = doc_dto  # Убираем дубли по ID
            else:
                custom_fields.append(FieldDTO.model_validate(field, from_attributes=True))

        return TemplateInfoDto(
            required_documents=list(documents.values()),
            custom_fields=custom_fields,
            id=template.id,
            name=template.name,
            name_ru=template.name_ru,
            description=template.description,
            image_url=template.image_url,
            download_url=template.download_url
        )
