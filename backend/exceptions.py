"""Custom exception classes and FastAPI exception handlers."""

from fastapi import Request
from fastapi.responses import JSONResponse


class ValidationError(Exception):
    """Raised when input validation fails (422)."""

    def __init__(self, detail: list[dict] | str):
        if isinstance(detail, str):
            self.detail = [{"field": "general", "message": detail}]
        else:
            self.detail = detail
        super().__init__(str(self.detail))


class ConflictError(Exception):
    """Raised when a resource already exists (409)."""

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class UnauthorizedError(Exception):
    """Raised when authentication fails (401)."""

    def __init__(self, detail: str = "Invalid credentials"):
        self.detail = detail
        super().__init__(detail)


class NotFoundError(Exception):
    """Raised when a resource is not found (404)."""

    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail
        super().__init__(detail)


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle ValidationError exceptions."""
    return JSONResponse(status_code=422, content={"detail": exc.detail})


async def conflict_error_handler(request: Request, exc: ConflictError) -> JSONResponse:
    """Handle ConflictError exceptions."""
    return JSONResponse(status_code=409, content={"detail": exc.detail})


async def unauthorized_error_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    """Handle UnauthorizedError exceptions."""
    return JSONResponse(status_code=401, content={"detail": exc.detail})


async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handle NotFoundError exceptions."""
    return JSONResponse(status_code=404, content={"detail": exc.detail})
