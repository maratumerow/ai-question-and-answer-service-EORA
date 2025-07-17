from src.application.dto.responses import (
    AnswerResponse,
    QuestionAnswerResponse,
    QuestionResponse,
    SourceResponse,
)
from src.domain.entities import Answer, Question, Source


class ResponseConverter:
    """Converter for domain entities to response DTOs."""

    @staticmethod
    def question_to_response(question: Question) -> QuestionResponse:
        """Convert domain Question to response schema."""
        return QuestionResponse(
            id=question.id,
            text=question.text,
            created_at=question.created_at,
        )

    @staticmethod
    def source_to_response(source: Source) -> SourceResponse:
        """Convert domain Source to response schema."""
        return SourceResponse(
            id=source.id,
            url=source.url,
            title=source.title,
            created_at=source.created_at,
            updated_at=source.updated_at,
        )

    @staticmethod
    def answer_to_response(answer: Answer) -> AnswerResponse:
        """Convert domain Answer to response schema."""
        return AnswerResponse(
            id=answer.id,
            question_id=answer.question_id,
            text=answer.text,
            created_at=answer.created_at,
            processing_time_ms=answer.processing_time_ms,
        )

    @staticmethod
    def question_answer_to_response(
        question: Question, answer: Answer
    ) -> QuestionAnswerResponse:
        """Convert domain Question and Answer to response schema."""
        return QuestionAnswerResponse(
            question=ResponseConverter.question_to_response(question),
            answer=ResponseConverter.answer_to_response(answer),
        )
