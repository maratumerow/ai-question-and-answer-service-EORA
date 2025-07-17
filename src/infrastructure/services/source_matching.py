import re

from src.domain.entities import Source
from src.domain.services import SourceMatchingServiceInterface


class SimpleSourceMatchingService(SourceMatchingServiceInterface):
    """Simple but effective implementation of SourceMatchingService."""

    def __init__(self) -> None:
        # Простой набор стоп-слов
        self.stop_words: set[str] = {
            "что",
            "как",
            "для",
            "это",
            "или",
            "при",
            "без",
            "где",
            "когда",
            "кто",
            "может",
            "можно",
            "есть",
            "был",
            "была",
            "было",
            "были",
            "будет",
            "будут",
            "если",
            "чтобы",
            "также",
            "тоже",
            "очень",
            "более",
            "самый",
            "такой",
            "который",
            "которая",
            "которое",
            "которые",
            "свой",
            "своя",
            "свое",
            "всех",
            "всем",
            "всё",
            "все",
            "той",
            "том",
            "тот",
            "эта",
            "эти",
            "нас",
            "нам",
            "наш",
            "наша",
            "наше",
            "наши",
            "вас",
            "вам",
            "ваш",
            "ваша",
            "ваше",
            "ваши",
            "его",
            "её",
            "их",
            "него",
            "неё",
            "них",
        }

    async def find_relevant_sources(
        self, question: str, sources: list[Source]
    ) -> list[Source]:
        """Find sources relevant to the question using improved matching."""
        if not sources:
            return []

        if not question.strip():
            return sources[:3]

        # Извлекаем ключевые слова из вопроса
        question_keywords = self._extract_keywords(question)

        if not question_keywords:
            return sources[:3]

        # Оцениваем релевантность каждого источника
        scored_sources: list[tuple[Source, float]] = []
        for source in sources:
            score = self._calculate_score(question_keywords, source)
            if score > 0:
                scored_sources.append((source, score))

        # Сортируем и возвращаем топ-5
        scored_sources.sort(key=lambda x: x[1], reverse=True)
        result = [source for source, _ in scored_sources[:5]]

        # Если ничего не найдено, возвращаем первые 3
        return result if result else sources[:3]

    def _extract_keywords(self, text: str) -> set[str]:
        """Extract meaningful keywords from text."""
        # Убираем знаки препинания и приводим к нижнему регистру
        clean_text = re.sub(r"[^\w\s]", " ", text.lower())
        words = clean_text.split()

        # Фильтруем короткие слова и стоп-слова
        return {
            word
            for word in words
            if len(word) > 2 and word not in self.stop_words
        }

    def _calculate_score(self, keywords: set[str], source: Source) -> float:
        """Calculate relevance score for a source."""
        # Объединяем заголовок и содержимое
        title_text = source.title.lower()
        content_text = source.content.lower()

        score = 0.0

        # Проверяем совпадения в заголовке (больший вес)
        for keyword in keywords:
            if keyword in title_text:
                score += 3.0

        # Проверяем совпадения в содержимом
        for keyword in keywords:
            if keyword in content_text:
                score += 1.0

        # Нормализуем по количеству ключевых слов
        return score / len(keywords) if keywords else 0.0
