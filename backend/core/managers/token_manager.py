import datetime
import os
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from core.models.models import User
from core.managers.database_manager import DatabaseManager

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]


class TokenManager:
    def __init__(self, database, email) -> None:
        self.database = (database,)
        self.email = email

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

    def _get_user(self):
        emails = [
            {"email": e.get("email"), "hashed_password": e.get("password")}
            for e in DatabaseManager(self.database[0]).read(User)
            if e.get("email") == self.email
        ]
        if self.email in emails[0].get("email"):
            return emails[0]
        return None

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, password: str):
        user = self._get_user()
        if not user:
            return False
        if not self.verify_password(password, user.get("hashed_password")):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
