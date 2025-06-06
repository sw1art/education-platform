from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.course.models import Tag


class TagDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_tag(self, name: str, color: str = "#007bff") -> Tag:
        new_tag = Tag(name=name, color=color)
        self.db_session.add(new_tag)
        await self.db_session.flush()
        return new_tag

    async def get_by_id(self, tag_id: int) -> Optional[Tag]:
        res = await self.db_session.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        return res.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Tag]:
        res = await self.db_session.execute(
            select(Tag).where(Tag.name == name)
        )
        return res.scalar_one_or_none()

    async def get_all(self) -> List[Tag]:
        res = await self.db_session.execute(select(Tag))
        return res.scalars().all()

    async def update_tag(self, tag_id: int, **kwargs) -> Optional[int]:
        if not kwargs:
            return None
        query = (
            update(Tag)
            .where(Tag.id == tag_id)
            .values(**kwargs)
            .returning(Tag.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()

    async def delete_tag(self, tag_id: int) -> Optional[int]:
        query = (
            delete(Tag)
            .where(Tag.id == tag_id)
            .returning(Tag.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()
