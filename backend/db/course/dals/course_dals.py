from typing import Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from db.course.models import Course, CourseStatus

class CourseDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_course(self, **kwargs) -> Course:
        new_course = Course(**kwargs)
        self.db_session.add(new_course)
        await self.db_session.flush()
        return new_course

    async def get_course_by_id(self, course_id: int) -> Optional[Course]:
        res = await self.db_session.execute(
            select(Course).where(Course.id == course_id)
        )
        return res.scalar_one_or_none()

    async def update_course(self, course_id: int, **kwargs) -> Optional[int]:
        if not kwargs:
            return None
        query = (
            update(Course)
            .where(Course.id == course_id)
            .values(**kwargs)
            .returning(Course.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()

    async def delete_course(self, course_id: int) -> Optional[int]:
        query = (
            delete(Course)
            .where(Course.id == course_id)
            .returning(Course.id)
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()

    async def list_published_courses(self, limit: int = 100, offset: int = 0):
        res = await self.db_session.execute(
            select(Course)
            .where(Course.status == CourseStatus.PUBLISHED)
            .limit(limit)
            .offset(offset)
        )
        return [row[0] for row in res.fetchall()]