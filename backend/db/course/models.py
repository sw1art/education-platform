from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class CourseStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class CourseDifficulty(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class LessonType(enum.Enum):
    VIDEO = "video"
    TEXT = "text"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"

class MaterialType(enum.Enum):
    PDF = "pdf"
    VIDEO = "video"
    AUDIO = "audio"
    LINK = "link"
    PRESENTATION = "presentation"
    CODE = "code"
    IMAGE = "image"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    slug = Column(String(110), unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    courses = relationship("Course", back_populates="category")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(250), unique=True, index=True)
    short_description = Column(String(500))
    description = Column(Text)
    thumbnail = Column(String(500))  # URL изображения
    trailer_video = Column(String(500))  # URL трейлера
    
    # Метаданные курса
    difficulty = Column(Enum(CourseDifficulty), default=CourseDifficulty.BEGINNER)
    status = Column(Enum(CourseStatus), default=CourseStatus.DRAFT)
    price = Column(Float, default=0.0)  # 0 = бесплатный курс
    estimated_duration = Column(Integer)  # в минутах
    language = Column(String(10), default="ru")
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    teacher_id = Column(UUID, ForeignKey("users.id")) 

    # Метаданные времени (из Base передается created_at и updated_at)
    published_at = Column(DateTime, nullable=True)
    
    # JSON поля
    tags = Column(JSON)  # ["tag 1", "tag 2", "tag 3" ...]
    learning_outcomes = Column(JSON)  # ["Освоите FastAPI", "Создадите REST API" ...] - список, что даст обучение
    requirements = Column(JSON)  # ["Базовые знания Python", "Установленный Python"] - список требований перед курсом к студентам
    
    category = relationship("Category", back_populates="courses")
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="course", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(250), index=True)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)  # порядок в курсе
    is_free = Column(Boolean, default=True)  # бесплатный/платный модуль
    
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(250), index=True)
    content = Column(Text)  # основной контент урока
    lesson_type = Column(Enum(LessonType), default=LessonType.TEXT)
    
    # Медиа контент
    video_url = Column(String)
    video_duration = Column(Integer)  # в секундах или в минутах сделать?
    
    # Метаданные урока
    order_index = Column(Integer, nullable=False)
    is_free = Column(Boolean, default=True) # бесплатный/платный лекция
    estimated_duration = Column(Integer)  # в минутах
    
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    
    # JSON поля
    notes = Column(JSON)  # заметки преподавателя
    resources = Column(JSON)  # ссылки на дополнительные ресурсы
    
    # Отношения
    module = relationship("Module", back_populates="lessons")
    materials = relationship("Material", back_populates="lesson", cascade="all, delete-orphan")

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    material_type = Column(Enum(MaterialType), nullable=False)
    
    # Файл или ссылка
    file_url = Column(String(500))
    file_size = Column(Integer)  # в байтах
    original_filename = Column(String(255))
    
    # Связи (материал может быть привязан к курсу или к уроку)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    
    # Метаданные
    is_downloadable = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    
    course = relationship("Course", back_populates="materials")
    lesson = relationship("Lesson", back_populates="materials")

# Дополнительная модель для тегов
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(7), default="#007bff")  # HEX цвет, пока так, далее на фронте сделаем как нужно


# Связующая таблица многие-ко-многим для курсов и тегов
class CourseTag(Base):
    __tablename__ = "course_tags"
    
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)