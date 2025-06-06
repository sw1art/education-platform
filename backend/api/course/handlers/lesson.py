from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.course.dals.lesson_dals import LessonDAL
from db.course.schemas import LessonCreate, LessonRead, LessonUpdate
from db.session import get_db

router = APIRouter()


@router.post("/", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson_in: LessonCreate,
    session: AsyncSession = Depends(get_db),
):
    async with LessonDAL(session) as dal:
        lesson = await dal.create(lesson_in)
        return lesson


@router.get("/", response_model=List[LessonRead])
async def read_lessons(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    async with LessonDAL(session) as dal:
        lessons = await dal.get_all(skip=skip, limit=limit)
        return lessons


@router.get("/{lesson_id}", response_model=LessonRead)
async def read_lesson(
    lesson_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with LessonDAL(session) as dal:
        lesson = await dal.get(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson


@router.put("/{lesson_id}", response_model=LessonRead)
async def update_lesson(
    lesson_id: int,
    lesson_in: LessonUpdate,
    session: AsyncSession = Depends(get_db),
):
    async with LessonDAL(session) as dal:
        lesson = await dal.get(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        updated_lesson = await dal.update(lesson, lesson_in)
        return updated_lesson


@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(
    lesson_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with LessonDAL(session) as dal:
        lesson = await dal.get(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        await dal.delete(lesson)
    return None
