from lawly_db.db_models import RefreshSession, User
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class RegisterDTO:
    refresh_session: RefreshSession
    user: User
    session: AsyncSession
