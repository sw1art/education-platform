import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import validator

from api.user.validators import (
    NameValidationMixin,
    SurnameValidationMixin,
    UsernameValidationMixin
    )


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    username: str
    email: EmailStr
    is_active: bool


class UserCreate(
    NameValidationMixin,
    SurnameValidationMixin,
    UsernameValidationMixin,
    TunedModel,
):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str


class UpdateUserRequest(
    NameValidationMixin,
    SurnameValidationMixin,
    UsernameValidationMixin,
    TunedModel,
):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    username: Optional[constr(min_length=1)]
    email: Optional[EmailStr]


class DeleteUserResponse(TunedModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(TunedModel):
    updated_user_id: uuid.UUID


class Token(TunedModel):
    access_token: str
    token_type: str