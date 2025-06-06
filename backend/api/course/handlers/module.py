from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.course.dals.module_dals import ModuleDAL
from db.course.schemas import ModuleCreate, ModuleRead, ModuleUpdate
from db.session import get_db

router = APIRouter()


@router.post("/", response_model=ModuleRead, status_code=status.HTTP_201_CREATED)
async def create_module(
    module_in: ModuleCreate,
    session: AsyncSession = Depends(get_db),
):
    async with ModuleDAL(session) as dal:
        module = await dal.create(module_in)
        return module


@router.get("/", response_model=List[ModuleRead])
async def read_modules(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    async with ModuleDAL(session) as dal:
        modules = await dal.get_all(skip=skip, limit=limit)
        return modules


@router.get("/{module_id}", response_model=ModuleRead)
async def read_module(
    module_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with ModuleDAL(session) as dal:
        module = await dal.get(module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        return module


@router.put("/{module_id}", response_model=ModuleRead)
async def update_module(
    module_id: int,
    module_in: ModuleUpdate,
    session: AsyncSession = Depends(get_db),
):
    async with ModuleDAL(session) as dal:
        module = await dal.get(module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        updated_module = await dal.update(module, module_in)
        return updated_module


@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(
    module_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with ModuleDAL(session) as dal:
        module = await dal.get(module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        await dal.delete(module)
    return None
