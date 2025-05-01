from lawly_db.db_models import DocumentCreation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository


class DocumentCreationRepository(BaseRepository):
    model = DocumentCreation

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_document_creation_by_id(
        self, user_id: int, document_creation_id: int
    ) -> model | None:
        """
        Возвращает шаблон документа по ID
        :param user_id: ID пользователя
        :param document_creation_id: ID создания документа
        :return: объект класса DocumentCreation
        """
        query = select(self.model).where(
            self.model.user_id == user_id, self.model.id == document_creation_id
        )
        _ = await self.session.execute(query)
        return _.scalar()
