from dataclasses import asdict, dataclass, replace
from datetime import datetime
from pprint import pprint
from typing import Optional

from fastapi import FastAPI, HTTPException, Path, status, Depends
from pydantic import BaseModel, Field
from database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from model import Todos as TodoModel

tags_metadata = [
    {
        "name": "todo",
        "description": "タスクに関する操作",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

BASE_SCHEMA_EXTRA = {
    "title": "サンプル",
    "description": "説明",
    "priority": 5,
    "complete": True,
}


class BaseTodo(BaseModel):
    title: str = Field(description="タスク名")
    description: str = Field(description="タスクの説明")
    priority: int = Field(description="タスクの重要度", gt=0, lt=6)
    complete: bool = Field(description="タスクが完了したかどうか")

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _: type["BaseTodo"]):
            schema["example"] = BASE_SCHEMA_EXTRA


class TodoIn(BaseTodo):
    pass


class TodoOut(BaseTodo):
    id: int = Field(description="タスクのID")
    created_at: datetime = Field(description="作成日時", default=datetime.now())
    updated_at: datetime = Field(description="更新日時", default=datetime.now())

    class Config:
        orm_mode = True
        
        @staticmethod
        def schema_extra(schema: dict, _: type["TodoOut"]):
            schema["example"] = {
                **BASE_SCHEMA_EXTRA,
                **{
                    "id": 1,
                    "create_at": datetime.today(),
                    "updated_at": datetime.today(),
                },
            }

@dataclass(frozen=True)        
class Todo:
    id: str
    title: str
    description: str
    priority: int
    complete: bool
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    def update(self, todo: TodoIn) -> type["Todo"]:
        updated_todo = todo.dict()
        return replace(self, **{**updated_todo, **{"updated_at": datetime.now()}})
    


TODOS = [
    Todo(id=1, title="テスト1", description="テストのTodo", priority=5, complete=False),
    Todo(id=2, title="テスト2", description="テストのTodo", priority=1, complete=False),
]


@app.get(
    "/todos",
    tags=["todo"],
    status_code=status.HTTP_200_OK,
    response_description="全てのタスク",
    response_model=list[TodoOut],
)
async def get_todos(db: Session = Depends(get_db)) -> list[TodoOut]:
    """
    タスクを全件取得する
    """
    
    todos = db.execute(select(TodoModel)).scalars().all()
    
    return todos


@app.get(
    "/todos/{todo_id}",
    tags=["todo"],
    status_code=status.HTTP_200_OK,
    response_description="１件のタスク",
    response_model=TodoOut
)
async def get_todo(todo_id: int = Path(gt=0), db: Session = Depends(get_db)) -> TodoOut:
    """
    タスクを１件取得する

    タスクのIDが存在しなかった場合エラー

    - **todo_id**: タスクのID
    """
    
    todo = db.execute(select(TodoModel).where(TodoModel.id == todo_id)).scalar()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="todo not found",
        )

    return todo


@app.post(
    "/todos",
    tags=["todo"],
    status_code=status.HTTP_200_OK,
    response_description="作成された Todo",
    response_model=TodoOut
)
async def create_todo(todo: TodoIn, db: Session = Depends(get_db)) -> TodoOut:
    """
    タスクを１件登録する

    既に登録済みのタスクIDが指定された場合エラー

    - **title**: タスク名
    - **description**: タスクの説明
    - **priority**: タスクの重要度
    - **complete**: タスクが完了したかどうか
    """
    
    todo_model = TodoModel(**todo.dict())
    
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    
    return todo_model


@app.put("/todos/{todo_id}", tags=["todo"], status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int, todo_in: TodoIn, db: Session = Depends(get_db)) -> None:
    """
    タスクを１件更新する

    登録済みのタスクID以外が指定された場合エラー

    - **id**: タスクのID
    - **title**: タスク名
    - **description**: タスクの説明
    - **priority**: タスクの重要度
    - **complete**: タスクが完了したかどうか
    """
    
    todo: TodoModel = db.execute(select(TodoModel).where(TodoModel.id == todo_id)).scalar()
    
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="todo not found",
        )
        
    todo.title = todo_in.title
    todo.description = todo_in.description
    todo.priority = todo_in.priority
    todo.complete = todo_in.complete
    todo.updated_at = datetime.today()
    
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo
