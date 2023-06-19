from datetime import datetime
from pprint import pprint
from typing import Optional

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

tags_metadata = [
    {
        "name": "todo",
        "description": "タスクに関する操作",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

BASE_SCHEMA_EXTRA = {
    "example": {
        "id": 1,
        "title": "サンプル",
        "description": "説明",
        "priority": 5,
        "complete": True,
    }
}


class BaseTodo(BaseModel):
    id: int = Field(description="タスクのID")
    title: str = Field(description="タスク名")
    description: str = Field(description="タスクの説明")
    priority: int = Field(description="タスクの重要度", gt=0, lt=6)
    complete: bool = Field(description="タスクが完了したかどうか")

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _: type["TodoOut"]):
            schema["example"] = BASE_SCHEMA_EXTRA


class TodoIn(BaseTodo):
    id: Optional[int] = Field(description="タスクのID")


class TodoOut(BaseTodo):
    created_at: datetime = Field(description="作成日時")

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _: type["TodoOut"]):
            schema["example"] = {
                **BASE_SCHEMA_EXTRA["example"],
                **{"create_at": datetime.today()},
            }


TODOS = [
    TodoIn(id=1, title="テスト1", description="テストのTodo", priority=5, complete=False),
    TodoIn(id=2, title="テスト2", description="テストのTodo", priority=1, complete=False),
]


@app.get(
    "/todos",
    tags=["todo"],
    status_code=status.HTTP_200_OK,
    response_description="全てのタスク",
)
async def get_todos() -> list[TodoOut]:
    """
    タスクを全件取得する
    """
    return TODOS


@app.get(
    "/todos/{todo_id}",
    tags=["todo"],
    status_code=status.HTTP_200_OK,
    response_description="１件のタスク",
)
async def get_todo(todo_id: int = Path(gt=0)) -> TodoOut:
    """
    タスクを１件取得する

    タスクのIDが存在しなかった場合エラー

    - **todo_id**: タスクのID
    """
    todo = next((x for x in TODOS if x.id == todo_id), None)

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="todo not found",
        )

    return todo


@app.post(
    "/todos",
    tags=["todo"],
    status_code=status.HTTP_201_CREATED,
    response_description="特になし",
)
async def create_todo(todo: TodoIn) -> None:
    """
    タスクを１件登録する

    既に登録済みのタスクIDが指定された場合エラー

    - **id**: タスクのID
        - 指定しない場合オートインクリメントする
    - **title**: タスク名
    - **description**: タスクの説明
    - **priority**: タスクの重要度
    - **complete**: タスクが完了したかどうか
    """

    if todo.id is None:
        todo.id = len(TODOS) + 1

    todo_ids = [x.id for x in TODOS]

    if todo.id in todo_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="id duplicated",
        )

    TODOS.append(todo)
