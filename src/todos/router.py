from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.todos import service
from src.todos.schemas import TodoCreate, TodoCreateResponse, TodoReadResponse

router = APIRouter(
    tags=["todo"],
    prefix="/todos",
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="全てのタスク",
    response_model=list[TodoReadResponse],
)
async def get_todos(db: Session = Depends(get_db)):
    """
    タスクを全件取得する
    """

    todos = service.fetch_all_todo(db)
    return todos


@router.get(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_description="１件のタスク",
    response_model=TodoReadResponse,
)
async def get_todo(db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    """
    タスクを１件取得する

    タスクのIDが存在しなかった場合エラー

    - **todo_id**: タスクのID
    """

    todo = service.fetch_todo(db, todo_id)

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
async def create_todo(todo_create: TodoCreate, db: Session = Depends(get_db)):
    """
    タスクを１件登録する

    既に登録済みのタスクIDが指定された場合エラー

    - **title**: タスク名
    - **description**: タスクの説明
    - **priority**: タスクの重要度
    - **complete**: タスクが完了したかどうか
    """
    new_todo = service.create_todo(db, todo_create)
    return new_todo


@router.put(
    "/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoCreateResponse
)
async def update_todo(
    todo_update: TodoCreate, todo_id: int, db: Session = Depends(get_db)
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

    original_todo = service.fetch_todo(db, todo_id)

    if original_todo is None:
        raise HTTPException(
            detail="Todo Not Found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    updated_todo = service.update_todo(db, todo_update, original_todo)

    return updated_todo
