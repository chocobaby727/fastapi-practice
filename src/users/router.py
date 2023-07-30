from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette import status

from src.database import db_dependency
from src.users import service
from src.users.jwt import (
    ALGORISM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    oauth2_token,
)
from src.users.schemas import CreateUserRequest, Token

router = APIRouter(tags=["users"], prefix="/users")


async def get_current_user(token: Annotated[str, Depends(oauth2_token)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORISM)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    username: str = payload.get("sub")
    user_id: int = payload.get("id")
    user_role: str = payload.get("role")

    if username is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    return {"username": username, "user_id": user_id, "user_role": user_role}


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    user_id = user["user_id"]
    user = service.fetch_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found."
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    """ユーザを作成する

    * **username** : 氏名
    * **email**: メールアドレス
    * **first_name**: 苗字
    * **last_name**: 名前
    * **password**: パスワード（内部でハッシュ化して利用）
    * **role**: 権限

    """
    service.create_user(db, create_user_request)


@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    authenticated_user = authenticate_user(form_data.username, form_data.password, db)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    token = create_access_token(
        authenticated_user.username,
        authenticated_user.id,
        authenticated_user.role,
        timedelta(minutes=20),
    )

    return {"access_token": token, "token_type": "bearer"}


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def change_password(
    user: user_dependency, db: db_dependency, plain_password=Body(example="test123")
):
    user_id = user["user_id"]
    user = service.fetch_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found."
        )

    service.edit_password(db, user, plain_password)
