from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.course.dals.tag_dals import TagDAL
from db.course.schemas import TagCreate, TagRead, TagUpdate
from db.session import get_db

router = APIRouter()


@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: TagCreate,
    session: AsyncSession = Depends(get_db),
):
    async with TagDAL(session) as dal:
        tag = await dal.create(tag_in)
        return tag


@router.get("/", response_model=List[TagRead])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    async with TagDAL(session) as dal:
        tags = await dal.get_all(skip=skip, limit=limit)
        return tags


@router.get("/{tag_id}", response_model=TagRead)
async def read_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with TagDAL(session) as dal:
        tag = await dal.get(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag


@router.put("/{tag_id}", response_model=TagRead)
async def update_tag(
    tag_id: int,
    tag_in: TagUpdate,
    session: AsyncSession = Depends(get_db),
):
    async with TagDAL(session) as dal:
        tag = await dal.get(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        updated_tag = await dal.update(tag, tag_in)
        return updated_tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with TagDAL(session) as dal:
        tag = await dal.get(tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        await dal.delete(tag)
    return None
