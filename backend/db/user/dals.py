from typing import Union
from uuid import UUID
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.user.models import PortalRole, User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        username: str,
        email: str,
        hashed_password: str,
        roles: list[PortalRole],
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            username=username,
            email=email,
            hashed_password=hashed_password,
            roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id = res.scalar_one_or_none()
        return deleted_user_id

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        res = await self.db_session.execute(select(User).where(User.user_id == user_id))
        return res.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        res = await self.db_session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Union[User, None]:
        res = await self.db_session.execute(select(User).where(User.username == username))
        return res.scalar_one_or_none()

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        if not kwargs:
            return None

        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(**kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        updated_user_id = res.scalar_one_or_none()
        return updated_user_id
    
    async def get_teachers(self, limit: int = 100, offset: int = 0) -> list[User]:
        query = (
            select(User)
            .where(and_(User.is_active == True, User.roles.contains([PortalRole.ROLE_TEACHER])))
            .limit(limit)
            .offset(offset)
        )
        res = await self.db_session.execute(query)
        return [row[0] for row in res.fetchall()]

    async def get_students(self, limit: int = 100, offset: int = 0) -> list[User]:
        query = (
            select(User)
            .where(and_(User.is_active == True, User.roles.contains([PortalRole.ROLE_STUDENT])))
            .limit(limit)
            .offset(offset)
        )
        res = await self.db_session.execute(query)
        return [row[0] for row in res.fetchall()]

    async def promote_to_teacher(self, user_id: UUID) -> Union[UUID, None]:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return None
        
        user.promote_to_teacher()
        await self.db_session.flush()
        return user.user_id

    async def enroll_as_student(self, user_id: UUID) -> Union[UUID, None]:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return None
        
        user.enroll_as_student()
        await self.db_session.flush()
        return user.user_id

    async def update_user_stats(self, user_id: UUID, completed_courses: int = None, earned_certificates: int = None) -> Union[UUID, None]:
        update_data = {}
        if completed_courses is not None:       
            update_data['total_courses_completed'] = completed_courses
        if earned_certificates is not None:
            update_data['total_certificates_earned'] = earned_certificates
        if not update_data:
            return None
        if update_data:
            return await self.update_user(user_id, **update_data)
        return user_id

    async def search_users(self, query_text: str, role_filter: PortalRole = None, limit: int = 50) -> list[User]:
        """Поиск пользователей по имени, фамилии или username"""
        search_query = (select(User).where(
        User.is_active == True,(
            User.name.ilike(f'%{query_text}%') |
            User.surname.ilike(f'%{query_text}%') |
            User.username.ilike(f'%{query_text}%')
        ))
        .limit(limit)
        )
        
        if role_filter:
            search_query = search_query.where(User.roles.contains([role_filter]))
        
        res = await self.db_session.execute(search_query)
        return [row[0] for row in res.fetchall()]