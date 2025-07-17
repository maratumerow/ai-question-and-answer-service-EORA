"""Prompt building utilities for LLM."""

from src.domain.entities import Source


class PromptBuilder:
    """Builds prompts for LLM."""

    def build_prompt_with_sources(
        self, question: str, sources: list[Source]
    ) -> str:
        """Create optimized prompt."""
        context = self._prepare_context(sources)
        return self._build_prompt_template(question, context, sources)

    def _prepare_context(self, sources: list[Source]) -> str:
        """Prepare context from sources."""
        context_parts: list[str] = []
        for i, source in enumerate(sources, 1):
            context_parts.append(
                f"[{i}] {source.title}\nURL: {source.url}\n{source.content}\n"
            )
        return "\n".join(context_parts)

    def _build_prompt_template(
        self, question: str, context: str, sources: list[Source]
    ) -> str:
        """Build prompt template."""
        source_list = "\n".join([f"- {s.title}: {s.url}" for s in sources])

        return f"""Вы - консультант компании EORA, которая занимается \
разработкой AI-решений.

ДОСТУПНЫЕ ИСТОЧНИКИ:
{source_list}


ПОЛНАЯ ИНФОРМАЦИЯ:
{context}

ВОПРОС: {question}

ПРАВИЛА ОТВЕТА:
1. Структурируйте ответ по пунктам с заголовками
2. Для каждого решения включайте прямую ссылку в формате:
   "• Название решения: URL_ссылка: описание решения"
3. Используйте только релевантные источники из списка выше
4. Будьте конкретными и точными
5. НЕ используйте номерные ссылки [1], [2] - только прямые URL

ПРИМЕР ФОРМАТА:
• Система рекомендаций: https://eora.ru/cases/kazanexpress: \
EORA разработала систему персональных рекомендаций для компании KazanExpress...

Ответ:

"""
