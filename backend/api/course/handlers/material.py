from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.course.dals.material_dals import MaterialDAL
from db.course.schemas import MaterialCreate, MaterialRead, MaterialUpdate
from db.session import get_db

router = APIRouter()


@router.post("/", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
async def create_material(
    material_in: MaterialCreate,
    session: AsyncSession = Depends(get_db),
):
    async with MaterialDAL(session) as dal:
        material = await dal.create(material_in)
        return material


@router.get("/", response_model=List[MaterialRead])
async def read_materials(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    async with MaterialDAL(session) as dal:
        materials = await dal.get_all(skip=skip, limit=limit)
        return materials


@router.get("/{material_id}", response_model=MaterialRead)
async def read_material(
    material_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with MaterialDAL(session) as dal:
        material = await dal.get(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        return material


@router.put("/{material_id}", response_model=MaterialRead)
async def update_material(
    material_id: int,
    material_in: MaterialUpdate,
    session: AsyncSession = Depends(get_db),
):
    async with MaterialDAL(session) as dal:
        material = await dal.get(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        updated_material = await dal.update(material, material_in)
        return updated_material


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(
    material_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with MaterialDAL(session) as dal:
        material = await dal.get(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        await dal.delete(material)
    return None
