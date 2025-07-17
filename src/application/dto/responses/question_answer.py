from pydantic import BaseModel

from .answer import AnswerResponse
from .question import QuestionResponse


class QuestionAnswerResponse(BaseModel):
    """Response object for complete Q&A."""

    question: QuestionResponse
    answer: AnswerResponse
