from passlib.context import CryptContext
import logging

# Заглушка для подавления предупреждений от bcrypt (т.к passlib "забросили")
# bcrypt==3.2.0 для того, чтобы не было предупреждений по дефолту
logging.getLogger('passlib').setLevel(logging.ERROR)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)