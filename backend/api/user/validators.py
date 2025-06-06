import re
from fastapi import HTTPException
from pydantic import validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
USERNAME_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z0-9_]+$")


class NameValidationMixin:
    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value


class SurnameValidationMixin:
    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contain only letters"
            )
        return value


class UsernameValidationMixin:
    @validator("username")
    def validate_username(cls, value):
        if not USERNAME_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Username may contain only letters, digits and underscores",
            )
        return value
