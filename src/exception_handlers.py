from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(exc.detail, status_code=exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    response = {}
    response["title"] = "validation failed."
    response["detail"] = "received invalid json syntax, invalid parameters."

    new_errors = []

    for _error in errors:
        error = {}

        error["name"] = ".".join(map(str, _error["loc"]))
        error["message"] = _error["msg"]
        error["type"] = _error["type"]

        if "ctx" in _error:
            error["ctx"] = _error["ctx"]

        new_errors.append(error)

    response["errors"] = new_errors
    response["body"] = exc.body

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(response),
    )
