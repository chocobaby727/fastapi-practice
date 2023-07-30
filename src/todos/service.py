from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.todos.models import Todo
from src.todos.schemas import TodoCreate


def fetch_all_todo(db: Session, user_id: int) -> list[Todo]:
    todos: list[Todo] = (
        db.execute(select(Todo).where(Todo.user_id == user_id)).scalars().all()
    )
    return todos


def fetch_todo(db: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    todo: Todo = db.execute(
        select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user_id)
    ).scalar()
    return todo


def create_todo(db: Session, todo_create: TodoCreate, user_id: str) -> Todo:
    new_todo = Todo(**todo_create.dict(), user_id=user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


def update_todo(db: Session, new_todo: TodoCreate, original_todo: Todo) -> Todo:
    original_todo.title = new_todo.title
    original_todo.description = new_todo.description
    original_todo.priority = new_todo.priority
    original_todo.complete = new_todo.complete
    original_todo.updated_at = datetime.today()

    db.add(original_todo)
    db.commit()
    db.refresh(original_todo)

    return original_todo


def delete_todo(db: Session, original_todo: Todo) -> None:
    db.delete(original_todo)
    db.commit()
