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


class GetTemplatesResponseDTO(BaseModel):
    total: int = Field(..., description="Общее количество доступных шаблонов")
    templates: list[TemplateDTO] = Field(..., description="Список доступных шаблонов")


class GetTemplateDTO(BaseModel):
    query: str | None = Field(None, description="Поисковый запрос")
    limit: int = Field(20, description="Максимальное количество возвращаемых шаблонов")
    offset: int = Field(0, description="Смещение для пагинации")


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


class DocumentDto(BaseModel):
    id: int = Field(..., description="Id документа")
    name: str = Field(..., description="Название документа")
    name_ru: str = Field(..., description="Название документа на русском")
    description: str = Field(..., description="Описание документа")

    fields: list[FieldDTO] = Field(..., description="Поля документа")

    class Config:
        from_attributes = True


class TemplateInfoDto(BaseModel):
    id: int = Field(..., description="Id шаблона")
    name: str = Field(..., description="Название шаблона")
    name_ru: str = Field(..., description="Название шаблона на русском")
    description: str = Field(..., description="Описание шаблона")
    image_url: str = Field(..., description="URL шаблона документа")
    download_url: str = Field(..., description="URL для скачивания шаблона")

    required_documents: list[DocumentDto] = Field(
        ..., description="Документы, связанные с шаблоном"
    )
    custom_fields: list[FieldDTO] = Field(..., description="Поля, связанные с шаблоном")

    class Config:
        from_attributes = True


class CreateTemplateDTO(BaseModel):
    user_id: int
    description: str


class DocumentCreationDTO(BaseModel):
    id: int = Field(..., description="Id документа")
    user_id: int = Field(..., description="Id пользователя")
    template_id: int = Field(..., description="Id шаблона")
    status: DocumentStatusEnum = Field(..., description="Статус документа")
    start_date: str = Field(..., description="Дата создания документа")
    end_date: str = Field(..., description="Дата завершения документа")
    custom_name: str = Field(..., description="Кастомное имя документа")
    error_message: str = Field(..., description="Сообщение об ошибке")


class TemplateDownloadDTO(BaseModel):
    download_url: str = Field(..., description="URL для скачивания шаблона")


class DownloadEmptyTemplateDTO(BaseModel):
    template_id: int = Field(..., description="Id шаблона")
