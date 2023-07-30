from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.users.models import User

SECRET_KEY = "d900c7a917ab3f51c04dec37283663be015d90aef3a1603a39642cbc80953184"
ALGORISM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_token = OAuth2PasswordBearer(tokenUrl="users/auth/token")


def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    user = db.execute(select(User).where(User.username == username)).scalar()

    if not user:
        return None

    is_authenticated = bcrypt_context.verify(password, user.hashed_password)

    if not is_authenticated:
        return None

    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORISM)
