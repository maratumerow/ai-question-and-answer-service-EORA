from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Request object for asking a question."""

    question: str = Field(
        min_length=1, max_length=1000, description="The question to ask"
    )
