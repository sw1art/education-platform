from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.course.dals.category_dals import CategoryDAL
from db.course.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from db.session import get_db

router = APIRouter()


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_db),
):
    async with CategoryDAL(session) as dal:
        category = await dal.create(category_in)
        return category


@router.get("/", response_model=list[CategoryRead])
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    async with CategoryDAL(session) as dal:
        categories = await dal.get_all(skip=skip, limit=limit)
        return categories


@router.get("/{category_id}", response_model=CategoryRead)
async def read_category(
    category_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with CategoryDAL(session) as dal:
        category = await dal.get(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    session: AsyncSession = Depends(get_db),
):
    async with CategoryDAL(session) as dal:
        category = await dal.get(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        updated_category = await dal.update(category, category_in)
        return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_db),
):
    async with CategoryDAL(session) as dal:
        category = await dal.get(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await dal.delete(category)
    return None
