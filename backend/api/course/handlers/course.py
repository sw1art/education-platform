from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from db.course.dals.course_dals import CourseDAL
from db.course.schemas import CourseCreate, CourseRead, CourseUpdate
from db.session import get_db

router = APIRouter()


# Получить список курсов (с пагинацией по offset-limit)
@router.get("/", response_model=List[CourseRead])
async def list_courses(
    offset: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_db),
):
    async with CourseDAL(session) as dal:
        courses = await dal.list(offset=offset, limit=limit)
        return courses


# Получить курс по id
@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    course_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with CourseDAL(session) as dal:
        course = await dal.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course


# Создать курс
@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    session: AsyncSession = Depends(get_db),
):
    async with CourseDAL(session) as dal:
        course = await dal.create(course_in)
        return course


# Обновить курс (полное обновление)
@router.put("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: int,
    course_in: CourseUpdate,
    session: AsyncSession = Depends(get_db),
):
    async with CourseDAL(session) as dal:
        course = await dal.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        updated_course = await dal.update(course, course_in)
        return updated_course


# Удалить курс
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with CourseDAL(session) as dal:
        course = await dal.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        await dal.delete(course)
        return None
