from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = {}


class APIResponse(BaseModel):
    ok: bool = True
    data: Any | None = None
    error: ErrorResponse | None = None
