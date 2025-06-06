from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.course.models import Module


class ModuleDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_module(
        self,
        title: str,
        slug: str,
        description: Optional[str],
        order_index: int,
        is_free: bool,
        course_id: int
    ) -> Module:
        new_module = Module(
            title=title,
            slug=slug,
            description=description,
            order_index=order_index,
            is_free=is_free,
            course_id=course_id
        )
        self.db_session.add(new_module)
        await self.db_session.flush()
        return new_module

    async def get_by_id(self, module_id: int) -> Optional[Module]:
        res = await self.db_session.execute(
            select(Module).where(Module.id == module_id)
        )
        return res.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Module]:
        res = await self.db_session.execute(
            select(Module).where(Module.slug == slug)
        )
        return res.scalar_one_or_none()

    async def get_by_course(self, course_id: int) -> List[Module]:
        res = await self.db_session.execute(
            select(Module)
            .where(Module.course_id == course_id)
            .order_by(Module.order_index)
        )
        return res.scalars().all()

    async def update_module(
        self,
        module_id: int,
        **kwargs
    ) -> Optional[int]:
        if not kwargs:
            return None
        query = (
            update(Module)
            .where(Module.id == module_id)
            .values(**kwargs)
            .returning(Module.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()

    async def delete_module(self, module_id: int) -> Optional[int]:
        query = (
            delete(Module)
            .where(Module.id == module_id)
            .returning(Module.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()
