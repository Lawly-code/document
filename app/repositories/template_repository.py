from lawly_db.db_models import Template
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository


class TemplateRepository(BaseRepository):
    model = Template

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_templates(
        self, query: str | None, limit: int, offset: int
    ) -> list[model]:
        """
        Возвращает список шаблонов документов по поисковому запросу
        """
        stmt = select(self.model)

        if query:
            stmt = stmt.where(
                func.lower(self.model.name_ru).ilike(f"%{query.lower()}%"),
                self.model.user_id.is_(None),
            )

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_total_documents(self, query: str | None) -> int:
        """
        Возвращает общее количество документов по поисковому запросу
        """
        stmt = select(func.count(self.model.id))

        if query:
            stmt = stmt.where(
                func.lower(self.model.name_ru).ilike(f"%{query.lower()}%")
            )

        result = await self.session.execute(stmt)
        return int(result.scalar())

    async def get_template_by_id(self, template_id: int) -> model | None:
        """
        Возвращает шаблон документа по ID
        """
        query = select(self.model).where(
            self.model.id == template_id, self.model.user_id.is_(None)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def create(self, entity: model):
        """
        Создает новый шаблон документа
        :param entity: объект шаблона
        :return: созданный шаблон
        """
        self.session.add(entity)
        await self.session.commit()
