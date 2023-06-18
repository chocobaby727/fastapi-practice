from typing import Optional

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel

tags_metadata = [
    {
        "name": "todo",
        "description": "タスクに関する操作",
    }
]

app = FastAPI(openapi_tags=tags_metadata)


# @dataclass
class TodoModel(BaseModel):
    id: Optional[int]
    title: str
    desctiption: str
    priority: int
    complete: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "サンプル",
                "description": "説明",
                "priority": 5,
                "complete": True,
            }
        }


TODOS = [
    TodoModel(id=1, title="テスト1", desctiption="テストのTodo", priority=5, complete=False),
    TodoModel(id=2, title="テスト2", desctiption="テストのTodo", priority=1, complete=False),
]


@app.get("/todos", tags=["todo"], status_code=status.HTTP_200_OK)
async def get_todos() -> list[TodoModel]:
    return TODOS


@app.get("/todos/{todo_id}", tags=["todo"], status_code=status.HTTP_200_OK)
async def get_todo(todo_id: int = Path(gt=0)) -> TodoModel:
    todo = next((x for x in TODOS if x.id == todo_id), None)

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="todo not found",
        )

    return todo
