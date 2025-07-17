import logging

from fastapi import Depends

from src.application.use_cases import (
    AskQuestionUseCase,
    CreateQuestionUseCase,
    FindRelevantSourcesUseCase,
    GenerateAnswerUseCase,
)
from src.domain.repositories import (
    AnswerRepositoryInterface,
    QuestionRepositoryInterface,
    SourceRepositoryInterface,
)
from src.domain.services import (
    LLMServiceInterface,
    SourceMatchingServiceInterface,
)
from src.presentation.dependencies.repositories import (
    get_answer_repository,
    get_question_repository,
    get_source_repository,
)
from src.presentation.dependencies.services import (
    get_anthropic_service,
    get_source_matching_service,
)

logger = logging.getLogger(__name__)


def get_create_question_use_case(
    question_repository: QuestionRepositoryInterface = Depends(
        get_question_repository
    ),
) -> CreateQuestionUseCase:
    """Get create question use case."""
    logger.debug("Creating CreateQuestionUseCase")
    return CreateQuestionUseCase(question_repository=question_repository)


def get_find_relevant_sources_use_case(
    source_repository: SourceRepositoryInterface = Depends(
        get_source_repository
    ),
    source_matching_service: SourceMatchingServiceInterface = Depends(
        get_source_matching_service
    ),
) -> FindRelevantSourcesUseCase:
    """Get find relevant sources use case."""
    logger.debug("Creating FindRelevantSourcesUseCase")
    return FindRelevantSourcesUseCase(
        source_repository=source_repository,
        source_matching_service=source_matching_service,
    )


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


def get_ask_question_use_case(
    create_question_use_case: CreateQuestionUseCase = Depends(
        get_create_question_use_case
    ),
    find_relevant_sources_use_case: FindRelevantSourcesUseCase = Depends(
        get_find_relevant_sources_use_case
    ),
    generate_answer_use_case: GenerateAnswerUseCase = Depends(
        get_generate_answer_use_case
    ),
) -> AskQuestionUseCase:
    """Get ask question use case."""
    logger.debug("Creating AskQuestionUseCase")
    return AskQuestionUseCase(
        create_question_use_case=create_question_use_case,
        find_relevant_sources_use_case=find_relevant_sources_use_case,
        generate_answer_use_case=generate_answer_use_case,
    )
