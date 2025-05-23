from datetime import datetime

from lawly_db.db_models.enum_models import DocumentStatusEnum
from pydantic import BaseModel, Field


class TemplateDTO(BaseModel):
    id: int = Field(..., description="Id шаблона")
    user_id: int | None = Field(
        None,
        description="Id пользователя, которому принадлежит шаблон(для кастомных шаблонов)",
    )
    name: str = Field(..., description="Название шаблона")
    name_ru: str = Field(..., description="Название шаблона на русском")
    description: str = Field(..., description="Описание шаблона")
    image_url: str = Field(..., description="URL шаблона документа")
    download_url: str = Field(..., description="URL для скачивания шаблона")


class DocumentCreateDto(BaseModel):
    template_id: int = Field(..., description="ID шаблона документа")
    custom_name: str = Field(..., description="Кастомное имя документа")


class DocumentCreateWithIdDTO(BaseModel):
    template_id: int = Field(..., description="ID шаблона документа")
    custom_name: str = Field(..., description="Кастомное имя документа")
    user_id: int = Field(..., description="ID пользователя, создающего документ")


class DocumentCreationResponseDTO(BaseModel):
    id: int = Field(..., description="ID документа")
    custom_name: str = Field(..., description="Название документа")
    user_id: int = Field(..., description="ID пользователя, создающего документ")
    template_id: int = Field(..., description="ID шаблона документа")
    status: DocumentStatusEnum = Field(..., description="Статус документа")
    start_date: datetime = Field(..., description="Дата создания документа")
    end_date: datetime | None = Field(None, description="Дата завершения документа")
    error_message: str | None = Field(None, description="Сообщение об ошибке")

    class Config:
        from_attributes = True


class DocumentCreationUpdateDTO(BaseModel):
    status: DocumentStatusEnum = Field(..., description="Статус документа")
    error_message: str | None = Field(None, description="Сообщение об ошибке")


class DocumentCreationUpdateWithUserIdDTO(DocumentCreationUpdateDTO):
    user_id: int = Field(..., description="ID пользователя, создающего документ")
    document_creation_id: int = Field(..., description="ID документа")


class DocumentDto(BaseModel):
    id: int = Field(..., description="ID документа")
    name: str = Field(..., description="Название документа")
    name_ru: str = Field(..., description="Название документа на русском")
    is_personal: bool = Field(..., description="Является ли документ персональным")
    link: str = Field(..., description="Ссылка на документ")
    description: str = Field(..., description="Описание документа")

    class Config:
        from_attributes = True


class FieldDTO(BaseModel):
    id: int = Field(..., description="ID поля")
    name: str = Field(..., description="Название поля", max_length=255)
    name_ru: str = Field(..., description="Название поля на русском", max_length=255)
    mask: str | None = Field(None, description="Маска поля", max_length=255)
    example: str | None = Field(None, description="Пример поля", max_length=255)
    filter_field: dict | None = Field(None, description="Фильтр поля")
    can_improve_ai: bool = Field(..., description="Можно ли улучшить поле с помощью ИИ")

    class Config:
        from_attributes = True


class DocumentStructureDTO(DocumentDto):
    fields: list[FieldDTO] = Field(..., description="Поля документа")


class ImproveTextDTO(BaseModel):
    text: str = Field(..., description="Текст для улучшения")


class ImproveTextWithUserIDDTO(ImproveTextDTO):
    user_id: int = Field(..., description="ID пользователя, отправившего текст")


class ImprovedTextResponseDTO(BaseModel):
    improved_text: str = Field(..., description="Улучшенный текст")


class GenerateDocumentFieldDTO(BaseModel):
    name: str = Field(..., description="Название поля")
    value: str = Field(..., description="Значение поля")


class GenerateDocumentDTO(BaseModel):
    template_id: int = Field(..., description="ID шаблона документа")
    fields: list[GenerateDocumentFieldDTO] = Field(..., description="Поля документа")
