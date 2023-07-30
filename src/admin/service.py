from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.todos.models import Todo
from src.todos.schemas import TodoCreate


def fetch_all_todo(db: Session) -> list[Todo]:
    todos: list[Todo] = db.execute(select(Todo)).scalars().all()
    return todos


def fetch_todo(db: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    todo: Todo = db.execute(
        select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user_id)
    ).scalar()
    return todo
