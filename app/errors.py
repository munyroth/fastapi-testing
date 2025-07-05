from typing import Any, Callable, Coroutine

from fastapi import FastAPI, status
from jwt import PyJWTError
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import JSONResponse


class InvalidCredentials(Exception):
    """User has provided the wrong username or password during log in."""

    pass


def create_exception_handler(
        status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]:
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Incorrect username or password",
                "error_code": "invalid_credentials",
            },
        ),
    )

    @app.exception_handler(PyJWTError)
    async def pyjwt__error(request, exc):
        return JSONResponse(
            content={
                "message": "Unauthorized access. Please check your credentials.",
                "error_code": "unauthorized_access",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
