import logging

from fastapi import APIRouter, Depends

from src.application.dto.requests import QuestionRequest
from src.application.dto.responses import QuestionAnswerResponse
from src.application.use_cases import AskQuestionUseCase
from src.presentation.dependencies import get_ask_question_use_case

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ask", response_model=QuestionAnswerResponse)
async def ask_question(
    request: QuestionRequest,
    use_case: AskQuestionUseCase = Depends(get_ask_question_use_case),
) -> QuestionAnswerResponse:
    """Ask a question and get an answer."""

    logger.info("Received question: %s", request.question)

    # Use case возвращает готовую DTO для презентации
    return await use_case.execute(request.question)
