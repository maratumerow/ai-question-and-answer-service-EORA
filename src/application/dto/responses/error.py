from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Response schema for errors."""

    error: str
    detail: str | None = None
