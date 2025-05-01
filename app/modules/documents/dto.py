from datetime import datetime

from lawly_db.db_models.enum_models import FieldTypeENum, DocumentStatusEnum
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
    link: str = Field(..., description="Ссылка на документ")
    description: str = Field(..., description="Описание документа")

    class Config:
        from_attributes = True


class FieldDTO(BaseModel):
    id: int = Field(..., description="ID поля")
    name: str = Field(..., description="Название поля", max_length=255)
    type: FieldTypeENum = Field(..., description="Тип поля")

    class Config:
        from_attributes = True


class DocumentStructureDTO(DocumentDto):
    fields: list[FieldDTO] = Field(..., description="Поля документа")


class ImproveTextDTO(BaseModel):
    text: str = Field(..., description="Текст для улучшения")


class ImprovedTextResponseDTO(BaseModel):
    improved_text: str = Field(..., description="Улучшенный текст")
