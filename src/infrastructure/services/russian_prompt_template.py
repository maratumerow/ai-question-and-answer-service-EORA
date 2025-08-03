"""Russian prompt template implementation."""

from src.domain.entities import Source
from src.domain.services.prompt_template import PromptTemplateInterface


class RussianPromptTemplate(PromptTemplateInterface):
    """Russian language prompt template."""

    def create_simple_prompt(self, question: str) -> str:
        """Create simple prompt for question only."""
        return f"Пожалуйста, ответьте на следующий вопрос: {question}"

    def create_context_prompt(
        self, question: str, sources: list[Source]
    ) -> str:
        """Create prompt with context from sources."""

        if not sources:
            return self.create_simple_prompt(question)

        # Build context from sources
        context_parts: list[str] = []
        for i, source in enumerate(sources, 1):
            context_parts.append(
                f"Источник {i} ({source.title}):\n{source.content}\n"
            )

        context = "\n".join(context_parts)

        return f"""Вы - консультант компании EORA, которая занимается \
разработкой AI-решений.

ИСТОЧНИКИ:
{context}

ВОПРОС: {question}

ПРАВИЛА ОТВЕТА:
1. Структурируйте ответ по пунктам с заголовками
2. Для каждого решения включайте прямую ссылку в формате:
   "• Название решения: URL_ссылка: описание решения"
3. Используйте только релевантные источники из списка выше
4. Будьте конкретными и точными
5. НЕ используйте номерные ссылки [1], [2] - только прямые URL
6. Указывай компанию клиента для которого было разработанно решение в ответе.

ПРИМЕР ФОРМАТА:
• Система рекомендаций: https://eora.ru/cases/kazanexpress: \
EORA разработала систему персональных рекомендаций для компании KazanExpress...

Ответ:

"""
