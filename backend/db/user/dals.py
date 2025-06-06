from typing import Union
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.user.models import PortalRole, User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        username: str,
        email: str,
        hashed_password: str,
        roles: list[PortalRole],
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            username=username,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id = res.scalar_one_or_none()
        return deleted_user_id

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        res = await self.db_session.execute(select(User).where(User.user_id == user_id))
        return res.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        res = await self.db_session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Union[User, None]:
        res = await self.db_session.execute(select(User).where(User.username == username))
        return res.scalar_one_or_none()

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        if not kwargs:
            return None

        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(**kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        updated_user_id = res.scalar_one_or_none()
        return updated_user_id
