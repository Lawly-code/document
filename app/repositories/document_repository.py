from lawly_db.db_models import Document
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository):
    model = Document

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all_documents(self) -> list[model]:
        """
        Возвращает все документы
        :return: список документов
        """
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_document_by_id(self, document_id: int) -> model | None:
        """
        Возвращает документ по id
        :param document_id: id документа
        :return: документ
        """
        query = select(self.model).where(self.model.id == document_id)
        result = await self.session.execute(query)
        return result.scalar()
