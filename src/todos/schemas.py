from datetime import datetime

from pydantic import BaseModel, Field

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


class TodoCreate(BaseTodo):
    class Config:
        @staticmethod
        def schema_extra(schema: dict, _: type["TodoCreate"]):
            schema["example"] = BASE_SCHEMA_EXTRA


class TodoCreateResponse(BaseTodo):
    id: int = Field(description="タスクのID")
    created_at: datetime = Field(description="作成日時", default=datetime.now())
    updated_at: datetime = Field(description="更新日時", default=datetime.now())

    class Config:
        orm_mode = True

        @staticmethod
        def schema_extra(schema: dict, _: type["TodoCreateResponse"]):
            schema["example"] = {
                **{
                    "id": 1,
                },
                **BASE_SCHEMA_EXTRA,
                **{
                    "create_at": datetime.today(),
                    "updated_at": datetime.today(),
                },
            }


class TodoReadResponse(TodoCreateResponse):
    pass
