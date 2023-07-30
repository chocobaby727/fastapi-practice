from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.admin import service
from src.database import db_dependency
from src.todos.schemas import TodoReadResponse
from src.users.router import get_current_user

router = APIRouter(
    tags=["admin"],
    prefix="/admin",
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    response_description="全てのタスク",
    response_model=list[TodoReadResponse],
)
async def get_todos(user: user_dependency, db: db_dependency):
    """
    全ユーザのタスクを全件取得する
    """

    user_role: int = user["user_role"]

    if user_role != "admin":
        raise HTTPException("UnAuthenticated", status_code=status.HTTP_401_UNAUTHORIZED)

    todos = service.fetch_all_todo(db)
    return todos
