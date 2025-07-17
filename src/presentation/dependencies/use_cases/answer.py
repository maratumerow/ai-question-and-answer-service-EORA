import logging

from fastapi import Depends

from src.application.use_cases import (
    GenerateAnswerUseCase,
)
from src.domain.repositories import (
    AnswerRepositoryInterface,
)
from src.domain.services import (
    LLMServiceInterface,
)
from src.presentation.dependencies.repositories import (
    get_answer_repository,
)
from src.presentation.dependencies.services import (
    get_anthropic_service,
)

logger = logging.getLogger(__name__)


def get_generate_answer_use_case(
    answer_repository: AnswerRepositoryInterface = Depends(
        get_answer_repository
    ),
    llm_service: LLMServiceInterface = Depends(get_anthropic_service),
) -> GenerateAnswerUseCase:
    """Get generate answer use case."""
    logger.debug("Creating GenerateAnswerUseCase")
    return GenerateAnswerUseCase(
        answer_repository=answer_repository,
        llm_service=llm_service,
    )
