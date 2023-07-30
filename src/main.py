from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.admin.router import router as admin_router
from src.exception_handlers import http_exception_handler, validation_exception_handler
from src.todos.router import router as todo_router
from src.users.router import router as user_router

app = FastAPI()


app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(todo_router)
