import uuid
from enum import Enum

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import declarative_base
from db.session import Base


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"   # Пользователь портала - базовая роль, доступ к общим функциям (если не запустил/не записался на курс)
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN" # Администратор портала - может управлять пользователями и контентом
    ROLE_TEACHER = "ROLE_TEACHER"        # Преподаватель - может создавать курсы
    ROLE_STUDENT = "ROLE_STUDENT"           # Студент - может проходить курсы (если запустил/записался на курс)
    ROLE_MODERATOR = "ROLE_MODERATOR"       # Модератор - может модерировать контент


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(MutableList.as_mutable(ARRAY(String)), nullable=False, default=[])
    avatar = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)


    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    @property
    def is_teacher(self) -> bool:
        return PortalRole.ROLE_TEACHER in self.roles

    @property
    def is_student(self) -> bool:
        return PortalRole.ROLE_STUDENT in self.roles

    @property
    def is_moderator(self) -> bool:
        return PortalRole.ROLE_MODERATOR in self.roles

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.surname}"

    def can_create_courses(self) -> bool:
        """Проверяет, может ли пользователь создавать курсы"""
        return self.is_teacher or self.is_moderator or self.is_admin

    def can_moderate_content(self) -> bool:
        """Проверяет, может ли пользователь модерировать контент"""
        return self.is_moderator or self.is_admin

    def add_role(self, role: PortalRole):
        """Добавляет роль пользователю, если её еще нет"""
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role: PortalRole):
        """Удаляет роль у пользователя"""
        if role in self.roles:
            self.roles = [r for r in self.roles if r != role]

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            self.roles.append(PortalRole.ROLE_PORTAL_ADMIN)

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            self.roles = [role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN]

    def promote_to_teacher(self):
        """Повышает пользователя до преподавателя"""
        self.add_role(PortalRole.ROLE_TEACHER)
        # Преподаватель также может быть студентом
        self.add_role(PortalRole.ROLE_STUDENT)

    def enroll_as_student(self):
        """Записывает пользователя как студента"""
        self.add_role(PortalRole.ROLE_STUDENT)

    def __repr__(self):
        return f"<User {self.username} ({self.email}) | Roles: {self.roles}>"