from typing import List, Optional
from pydantic import BaseModel, HttpUrl, constr, confloat, conint
from uuid import UUID
from datetime import datetime
from enum import Enum
from db.course.models import CourseStatus, CourseDifficulty, LessonType, MaterialType


class CategoryBase(BaseModel):
    name: str
    description: Optional[str]
    slug: str
    parent_id: Optional[int]
    is_active: Optional[bool] = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    class Config:
        from_attributes = True
    
class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class TagBase(BaseModel):
    name: str
    color: Optional[str] = "#007bff"


class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    class Config:
        from_attributes = True


class TagRead(TagBase):
    id: int

    class Config:
        from_attributes = True


class MaterialBase(BaseModel):
    title: str
    description: Optional[str]
    material_type: MaterialType
    file_url: Optional[HttpUrl]
    file_size: Optional[int]
    original_filename: Optional[str]
    is_downloadable: Optional[bool] = True
    order_index: Optional[int] = 0


class MaterialCreate(MaterialBase):
    course_id: Optional[int]
    lesson_id: Optional[int]

class MaterialUpdate(MaterialBase):
    class Config:
        from_attributes = True


class MaterialRead(MaterialBase):
    id: int
    course_id: Optional[int]
    lesson_id: Optional[int]

    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    slug: Optional[str]
    content: Optional[str]
    lesson_type: LessonType = LessonType.TEXT
    video_url: Optional[HttpUrl]
    video_duration: Optional[int]  # в секундах, сделать часы + минуты + секунды?
    order_index: int
    is_free: Optional[bool] = True
    estimated_duration: Optional[int]  # в секундах, сделать часы + минуты + секунды?
    notes: Optional[List[str]] = []
    resources: Optional[List[str]] = []

class LessonUpdate(LessonBase):
    class Config:
        from_attributes = True


class LessonCreate(LessonBase):
    module_id: int


class LessonRead(LessonBase):
    id: int
    module_id: int
    materials: List[MaterialRead] = []

    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    title: str
    slug: Optional[str]
    description: Optional[str]
    order_index: int
    is_free: Optional[bool] = True


class ModuleCreate(ModuleBase):
    course_id: int


class ModuleUpdate(ModuleBase):
    class Config:
        from_attributes = True


class ModuleRead(ModuleBase):
    id: int
    course_id: int
    lessons: List[LessonRead] = []

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str
    slug: Optional[str]
    short_description: Optional[str]
    description: Optional[str]
    thumbnail: Optional[HttpUrl]
    trailer_video: Optional[HttpUrl]
    difficulty: CourseDifficulty = CourseDifficulty.BEGINNER
    status: CourseStatus = CourseStatus.DRAFT
    price: float = 0.0
    estimated_duration: Optional[int]  # в минутах
    language: Optional[str] = "ru"
    published_at: Optional[datetime]
    tags: Optional[List[str]] = []
    learning_outcomes: Optional[List[str]] = []
    requirements: Optional[List[str]] = []


class CourseCreate(CourseBase):
    category_id: Optional[int]
    teacher_id: Optional[UUID]


class CourseUpdate(BaseModel):
    title: Optional[constr(max_length=200)]
    slug: Optional[constr(max_length=250)]
    short_description: Optional[constr(max_length=500)]
    description: Optional[str]
    thumbnail: Optional[constr(max_length=500)]
    trailer_video: Optional[constr(max_length=500)]

    difficulty: Optional[CourseDifficulty]
    status: Optional[CourseStatus]
    price: Optional[confloat(ge=0)]
    estimated_duration: Optional[conint(ge=0)]
    language: Optional[constr(max_length=10)]

    category_id: Optional[int]
    teacher_id: Optional[UUID]

    tags: Optional[List[str]]
    learning_outcomes: Optional[List[str]]
    requirements: Optional[List[str]]

    class Config:
        from_attributes = True


class CourseRead(CourseBase):
    id: int
    category: Optional[CategoryRead]
    modules: List[ModuleRead] = []
    materials: List[MaterialRead] = []

    class Config:
        from_attributes = True