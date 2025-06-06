from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.course.models import Material


class MaterialDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_material(
        self,
        title: str,
        description: Optional[str],
        material_type: str,
        file_url: Optional[str],
        file_size: Optional[int],
        original_filename: Optional[str],
        course_id: Optional[int] = None,
        lesson_id: Optional[int] = None,
        is_downloadable: bool = True,
        order_index: int = 0,
    ) -> Material:
        new_material = Material(
            title=title,
            description=description,
            material_type=material_type,
            file_url=file_url,
            file_size=file_size,
            original_filename=original_filename,
            course_id=course_id,
            lesson_id=lesson_id,
            is_downloadable=is_downloadable,
            order_index=order_index,
        )
        self.db_session.add(new_material)
        await self.db_session.flush()
        return new_material

    async def get_by_id(self, material_id: int) -> Optional[Material]:
        res = await self.db_session.execute(
            select(Material).where(Material.id == material_id)
        )
        return res.scalar_one_or_none()

    async def get_by_course(self, course_id: int) -> List[Material]:
        res = await self.db_session.execute(
            select(Material)
            .where(Material.course_id == course_id)
            .order_by(Material.order_index)
        )
        return res.scalars().all()

    async def get_by_lesson(self, lesson_id: int) -> List[Material]:
        res = await self.db_session.execute(
            select(Material)
            .where(Material.lesson_id == lesson_id)
            .order_by(Material.order_index)
        )
        return res.scalars().all()

    async def update_material(self, material_id: int, **kwargs) -> Optional[int]:
        if not kwargs:
            return None
        query = (
            update(Material)
            .where(Material.id == material_id)
            .values(**kwargs)
            .returning(Material.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()

    async def delete_material(self, material_id: int) -> Optional[int]:
        query = (
            delete(Material)
            .where(Material.id == material_id)
            .returning(Material.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()
