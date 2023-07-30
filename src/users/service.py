from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.users.jwt import bcrypt_context
from src.users.models import User
from src.users.schemas import CreateUserRequest


def create_user(db: Session, create_user_request: CreateUserRequest) -> None:
    new_user = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def fetch_user(db: Session, user_id: int) -> Optional[User]:
    user = db.execute(select(User).where(User.id == user_id)).scalar()
    return user


def edit_password(db: Session, original_user: User, plain_password: str) -> None:
    hashed_password = bcrypt_context.hash(plain_password)
    original_user.hashed_password = hashed_password

    db.add(original_user)
    db.commit()
    db.refresh(original_user)
