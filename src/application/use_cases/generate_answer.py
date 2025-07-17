import time
import uuid
from datetime import UTC, datetime

from src.domain.entities import Answer, Question, Source
from src.domain.repositories import (
    AnswerRepositoryInterface,
)
from src.domain.services import (
    LLMServiceInterface,
)


class GenerateAnswerUseCase:
    """Use case for generating answers."""

    def __init__(
        self,
        answer_repository: AnswerRepositoryInterface,
        llm_service: LLMServiceInterface,
    ):
        self.answer_repository = answer_repository
        self.llm_service = llm_service

    async def execute(
        self, question: Question, sources: list[Source] | None = None
    ) -> Answer:
        """Generate and save answer for a question."""
        start_time = time.time()

        # Generate answer with or without sources
        if sources:
            answer_text = await self.llm_service.generate_answer_with_sources(
                question.text, sources
            )
        else:
            answer_text = await self.llm_service.generate_answer(question.text)

        # Create answer
        processing_time = int((time.time() - start_time) * 1000)
        return await self.answer_repository.create(
            Answer(
                id=uuid.uuid4(),
                question_id=question.id,
                text=answer_text,
                created_at=datetime.now(UTC),
                processing_time_ms=processing_time,
            )
        )
