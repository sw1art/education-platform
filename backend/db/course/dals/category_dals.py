from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.course.models import Category


class CategoryDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_category(
        self,
        name: str,
        slug: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None,
        is_active: bool = True
    ) -> Category:
        new_category = Category(
            name=name,
            slug=slug,
            description=description,
            parent_id=parent_id,
            is_active=is_active
        )
        self.db_session.add(new_category)
        await self.db_session.flush()
        return new_category

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        res = await self.db_session.execute(
            select(Category).where(Category.id == category_id)
        )
        return res.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        res = await self.db_session.execute(
            select(Category).where(Category.slug == slug)
        )
        return res.scalar_one_or_none()

    async def get_all_active(self) -> List[Category]:
        res = await self.db_session.execute(
            select(Category).where(Category.is_active.is_(True))
        )
        return res.scalars().all()

    async def get_subcategories(self, parent_id: int) -> List[Category]:
        res = await self.db_session.execute(
            select(Category).where(Category.parent_id == parent_id)
        )
        return res.scalars().all()

    async def update_category(
        self,
        category_id: int,
        **kwargs
    ) -> Optional[int]:
        if not kwargs:
            return None
        query = (
            update(Category)
            .where(Category.id == category_id)
            .values(**kwargs)
            .returning(Category.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()

    async def delete_category(self, category_id: int) -> Optional[int]:
        query = (
            delete(Category)
            .where(Category.id == category_id)
            .returning(Category.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()
