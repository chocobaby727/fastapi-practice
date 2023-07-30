from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.database import db_dependency
from src.todos import service
from src.todos.schemas import TodoCreate, TodoCreateResponse, TodoReadResponse
from src.users.router import get_current_user

router = APIRouter(
    tags=["todos"],
    prefix="/todos",
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="全てのタスク",
    response_model=list[TodoReadResponse],
)
async def get_todos(user: user_dependency, db: db_dependency):
    """
    タスクを全件取得する
    """

    user_id: int = user["user_id"]

    todos = service.fetch_all_todo(db, user_id)
    return todos


@router.get(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_description="１件のタスク",
    response_model=TodoReadResponse,
)
async def get_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    """
    タスクを１件取得する

    タスクのIDが存在しなかった場合エラー

    - **todo_id**: タスクのID
    """

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    user_id: int = user["user_id"]

    todo = service.fetch_todo(db, todo_id, user_id)

    if todo is None:
        raise HTTPException(
            detail="Todo Not Found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return todo


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="作成された Todo",
    response_model=TodoCreateResponse,
)
async def create_todo(
    todo_create: TodoCreate, user: user_dependency, db: db_dependency
):
    """
    タスクを１件登録する

    既に登録済みのタスクIDが指定された場合エラー

    - **title**: タスク名
    - **description**: タスクの説明
    - **priority**: タスクの重要度
    - **complete**: タスクが完了したかどうか
    """

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    user_id: int = user["user_id"]

    new_todo = service.create_todo(db, todo_create, user_id)
    return new_todo


@router.put(
    "/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoCreateResponse
)
async def update_todo(
    todo_update: TodoCreate, todo_id: int, db: db_dependency, user: user_dependency
):
    """
    タスクを１件更新する

    登録済みのタスクID以外が指定された場合エラー

    - **id**: タスクのID
    - **title**: タスク名
    - **description**: タスクの説明
    - **priority**: タスクの重要度
    - **complete**: タスクが完了したかどうか
    """

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    user_id: int = user["user_id"]

    original_todo = service.fetch_todo(db, todo_id, user_id)

    if original_todo is None:
        raise HTTPException(
            detail="Todo Not Found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    updated_todo = service.update_todo(db, todo_update, original_todo)

    return updated_todo


@router.delete(
    "/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_todo(todo_id: int, db: db_dependency, user: user_dependency):
    """
    タスクを１件削除する

    タスクのIDが存在しなかった場合エラー

    - **todo_id**: タスクのID
    """

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    user_id: int = user["user_id"]

    original_todo = service.fetch_todo(db, todo_id, user_id)

    if original_todo is None:
        raise HTTPException(
            detail="Todo Not Found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    service.delete_todo(db, original_todo)
