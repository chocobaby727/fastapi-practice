import sys
from pathlib import Path

from sqlalchemy import create_engine

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.todos.models import Base as TodoBase
from src.users.models import Base as UserBase

DB_URL = "mysql+pymysql://root@db:3306/sample?charset=utf8"

db_engine = create_engine(DB_URL, echo=True)


def reset_database():
    UserBase.metadata.drop_all(bind=db_engine)
    UserBase.metadata.create_all(bind=db_engine)

    TodoBase.metadata.drop_all(bind=db_engine)
    TodoBase.metadata.create_all(bind=db_engine)


if __name__ == "__main__":
    reset_database()
