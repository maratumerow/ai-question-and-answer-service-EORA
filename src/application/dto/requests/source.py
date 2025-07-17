from pydantic import BaseModel, Field


class LoadSourcesRequest(BaseModel):
    """Request object for loading sources."""

    urls: list[str] = Field(min_length=1, description="List of URLs to load")
