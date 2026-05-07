from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pymongo.errors import PyMongoError


class NISFError(Exception):
    status_code = 400
    code = "nisf_error"

    def __init__(self, message: str, details: dict | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(NISFError):
    status_code = 404
    code = "not_found"


class UnsafeContentError(NISFError):
    status_code = 422
    code = "unsafe_content"


def _sanitize_validation_details(details: list[dict]) -> list[dict]:
    sanitized: list[dict] = []
    for item in details:
        clean_item: dict = {}
        for key, value in item.items():
            if key == "ctx" and isinstance(value, dict):
                clean_item[key] = {ctx_key: str(ctx_value) for ctx_key, ctx_value in value.items()}
            else:
                clean_item[key] = value
        sanitized.append(clean_item)
    return sanitized


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NISFError)
    async def nisf_exception_handler(request: Request, exc: NISFError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"ok": False, "error": {"code": exc.code, "message": exc.message, "details": exc.details}},
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "ok": False,
                "error": {
                    "code": "validation_error",
                    "message": "Invalid payload",
                    "details": _sanitize_validation_details(exc.errors()),
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "ok": False,
                "error": {
                    "code": "validation_error",
                    "message": "Invalid payload",
                    "details": _sanitize_validation_details(exc.errors()),
                },
            },
        )

    @app.exception_handler(PyMongoError)
    async def database_exception_handler(request: Request, exc: PyMongoError) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={
                "ok": False,
                "error": {
                    "code": "database_error",
                    "message": "Database operation failed",
                    "details": {"error": str(exc)},
                },
            },
        )
