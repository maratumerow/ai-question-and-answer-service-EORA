from src.application.dto.converters import ResponseConverter
from src.application.dto.responses import QuestionAnswerResponse
from src.application.use_cases.create_question import CreateQuestionUseCase
from src.application.use_cases.find_relevant_sources import (
    FindRelevantSourcesUseCase,
)
from src.application.use_cases.generate_answer import GenerateAnswerUseCase


class AskQuestionUseCase:
    """Use case for asking a question and getting an answer."""

    def __init__(
        self,
        create_question_use_case: CreateQuestionUseCase,
        find_relevant_sources_use_case: FindRelevantSourcesUseCase,
        generate_answer_use_case: GenerateAnswerUseCase,
    ):
        self.create_question_use_case = create_question_use_case
        self.find_relevant_sources_use_case = find_relevant_sources_use_case
        self.generate_answer_use_case = generate_answer_use_case

    async def execute(self, question_text: str) -> QuestionAnswerResponse:
        """Execute the use case and return response DTO."""
        # Create question
        question = await self.create_question_use_case.execute(question_text)

        # Find relevant sources
        relevant_sources = await self.find_relevant_sources_use_case.execute(
            question_text
        )

        # Generate answer using relevant sources
        answer = await self.generate_answer_use_case.execute(
            question, relevant_sources
        )

        # Convert to response DTO
        return ResponseConverter.question_answer_to_response(question, answer)
