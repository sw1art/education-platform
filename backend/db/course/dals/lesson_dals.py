from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db.course.models import Lesson


class LessonDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_lesson(
        self,
        title: str,
        slug: str,
        content: str,
        lesson_type: str,
        video_url: Optional[str],
        video_duration: Optional[int],
        order_index: int,
        is_free: bool,
        estimated_duration: Optional[int],
        module_id: int,
        notes: Optional[List[str]] = None,
        resources: Optional[List[str]] = None,
    ) -> Lesson:
        new_lesson = Lesson(
            title=title,
            slug=slug,
            content=content,
            lesson_type=lesson_type,
            video_url=video_url,
            video_duration=video_duration,
            order_index=order_index,
            is_free=is_free,
            estimated_duration=estimated_duration,
            module_id=module_id,
            notes=notes,
            resources=resources,
        )
        self.db_session.add(new_lesson)
        await self.db_session.flush()
        return new_lesson

    async def get_by_id(self, lesson_id: int) -> Optional[Lesson]:
        res = await self.db_session.execute(
            select(Lesson).where(Lesson.id == lesson_id)
        )
        return res.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Lesson]:
        res = await self.db_session.execute(
            select(Lesson).where(Lesson.slug == slug)
        )
        return res.scalar_one_or_none()

    async def get_by_module(self, module_id: int) -> List[Lesson]:
        res = await self.db_session.execute(
            select(Lesson)
            .where(Lesson.module_id == module_id)
            .order_by(Lesson.order_index)
        )
        return res.scalars().all()

    async def update_lesson(self, lesson_id: int, **kwargs) -> Optional[int]:
        if not kwargs:
            return None
        query = (
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(**kwargs)
            .returning(Lesson.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()

    async def delete_lesson(self, lesson_id: int) -> Optional[int]:
        query = (
            delete(Lesson)
            .where(Lesson.id == lesson_id)
            .returning(Lesson.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()
