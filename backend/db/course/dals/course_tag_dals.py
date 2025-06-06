from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from db.course.models import CourseTag


class CourseTagDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_tag_to_course(self, course_id: int, tag_id: int) -> None:
        stmt = insert(CourseTag).values(course_id=course_id, tag_id=tag_id)
        await self.db_session.execute(stmt)
        await self.db_session.flush()

    async def remove_tag_from_course(self, course_id: int, tag_id: int) -> None:
        stmt = (
            delete(CourseTag)
            .where(CourseTag.course_id == course_id)
            .where(CourseTag.tag_id == tag_id)
        )
        await self.db_session.execute(stmt)
        await self.db_session.flush()

    async def get_tags_for_course(self, course_id: int) -> List[int]:
        stmt = select(CourseTag.tag_id).where(CourseTag.course_id == course_id)
        result = await self.db_session.execute(stmt)
        return [row[0] for row in result.fetchall()]

    async def get_courses_for_tag(self, tag_id: int) -> List[int]:
        stmt = select(CourseTag.course_id).where(CourseTag.tag_id == tag_id)
        result = await self.db_session.execute(stmt)
        return [row[0] for row in result.fetchall()]
