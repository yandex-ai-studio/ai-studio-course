"""
arXiv MCP Server

MCP-сервер для поиска и получения информации о научных статьях на arXiv.

Запуск:
    python arxiv_mcp.py
"""

import os
import re
from datetime import date, datetime, timezone

import requests
import feedparser
from fastmcp import FastMCP

# Сетевые настройки передаются при запуске, а не в конструктор FastMCP.
ARXIV_HOST = os.getenv("ARXIV_HOST", "0.0.0.0")
ARXIV_PORT = int(os.getenv("ARXIV_PORT", "8000"))

# Создаём MCP сервер
mcp = FastMCP("ArxivResearch")

# Базовый URL для arXiv API
ARXIV_API_URL = "https://export.arxiv.org/api/query"

# Маппинг полей для поиска
FIELD_MAP = {
    "all": "all",
    "title": "ti",
    "abstract": "abs",
    "author": "au"
}


def _build_search_query(
    search_query: str, date_from: str | None, date_to: str | None
) -> str:
    """Добавить включительный диапазон дат первой подачи (UTC)."""
    if date_from is None and date_to is None:
        return search_query

    dates = {}
    for name, value in (("date_from", date_from), ("date_to", date_to)):
        if value is None:
            continue
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            raise ValueError(f"{name}: укажите дату в формате YYYY-MM-DD.")
        try:
            dates[name] = date.fromisoformat(value)
        except ValueError:
            raise ValueError(f"{name}: некорректная календарная дата '{value}'.") from None

    start = dates.get("date_from", date(1991, 1, 1))
    end = dates.get("date_to", datetime.now(timezone.utc).date())
    if start > end:
        raise ValueError(
            f"Начало диапазона ({start.isoformat()}) не может быть позже "
            f"конца ({end.isoformat()})."
        )

    start_formatted = start.isoformat().replace("-", "")
    end_formatted = end.isoformat().replace("-", "")
    return (
        f"({search_query}) AND "
        f"submittedDate:[{start_formatted}0000 TO {end_formatted}2359]"
    )


@mcp.tool()
def search_arxiv(
    query: str,
    field: str = "all",
    max_results: int = 3,
    date_from: str | None = None,
    date_to: str | None = None,
) -> str:
    """
    Поиск научных статей на arXiv по ключевым словам.
    Возвращает топ-N наиболее релевантных статей.
    
    Args:
        query: Поисковый запрос на английском языке. Ключевые слова через пробел.
        field: Поле для поиска: all (все поля), title (заголовок), abstract (аннотация), author (автор)
        max_results: Максимальное количество результатов (по умолчанию 3)
        date_from: Дата первой подачи от YYYY-MM-DD включительно (UTC); без неё — с 1991-01-01, если задана date_to.
        date_to: Дата первой подачи до YYYY-MM-DD включительно (UTC); без неё — по сегодня, если задана date_from.
            Одинаковые границы выбирают один день. Без обеих дат фильтра нет.
    """
    return _search_arxiv(query, field, max_results, date_from, date_to)


def _search_arxiv(
    query: str,
    field: str,
    max_results: int,
    date_from: str | None,
    date_to: str | None,
) -> str:
    """Общая реализация поиска для MCP-инструментов поиска и автора."""
    # Формируем поисковый запрос
    field_prefix = FIELD_MAP.get(field, "all")
    try:
        search_query = _build_search_query(f"{field_prefix}:{query}", date_from, date_to)
    except ValueError as e:
        return f"Ошибка в параметрах поиска: {e}"
    
    # Формируем параметры запроса
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=15)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            return "Статьи по данному запросу не найдены."
        
        results = []
        for i, entry in enumerate(feed.entries, 1):
            arxiv_id = entry.id.split('/abs/')[-1]
            authors = ', '.join(a.name for a in entry.authors[:3])
            if len(entry.authors) > 3:
                authors += " и др."
            
            # Укорачиваем аннотацию
            summary = entry.summary.replace('\n', ' ')[:300]
            
            results.append(
                f"{i}. **{entry.title}**\n"
                f"   - arXiv ID: {arxiv_id}\n"
                f"   - Авторы: {authors}\n"
                f"   - Аннотация: {summary}...\n"
            )
        
        total = feed.feed.opensearch_totalresults
        return f"Найдено статей: {total}. Топ-{max_results}:\n\n" + "\n".join(results)
    
    except Exception as e:
        return f"Ошибка при запросе к arXiv: {str(e)}"


@mcp.tool()
def get_paper_details(arxiv_id: str) -> str:
    """
    Получить полную информацию о статье по её arXiv ID,
    включая полную аннотацию, авторов, категории и ссылки.
    
    Args:
        arxiv_id: Идентификатор статьи на arXiv (например, 2304.12345 или 1706.03762)
    """
    # Очищаем ID от возможных префиксов
    arxiv_id = arxiv_id.replace("arXiv:", "").strip()
    
    params = {
        "id_list": arxiv_id,
        "max_results": 1
    }
    
    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=15)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            return f"Статья с ID {arxiv_id} не найдена."
        
        entry = feed.entries[0]
        authors = ', '.join(a.name for a in entry.authors)
        categories = ', '.join(t['term'] for t in entry.tags)
        
        # Получаем ссылки
        pdf_link = ""
        abs_link = ""
        for link in entry.links:
            if link.get('title') == 'pdf':
                pdf_link = link.href
            if link.rel == 'alternate':
                abs_link = link.href
        
        result = (
            f"**{entry.title}**\n\n"
            f"**arXiv ID:** {arxiv_id}\n"
            f"**Авторы:** {authors}\n"
            f"**Опубликовано:** {entry.published}\n"
            f"**Категории:** {categories}\n"
            f"**Ссылка на статью:** {abs_link}\n"
            f"**Ссылка на PDF:** {pdf_link}\n\n"
            f"**Аннотация:**\n{entry.summary}"
        )
        
        return result
    
    except Exception as e:
        return f"Ошибка при запросе к arXiv: {str(e)}"


@mcp.tool()
def search_by_author(
    author_name: str,
    max_results: int = 5,
    date_from: str | None = None,
    date_to: str | None = None,
) -> str:
    """
    Поиск статей конкретного автора на arXiv.
    
    Args:
        author_name: Имя автора (например, "Hinton" или "Yann LeCun")
        max_results: Максимальное количество результатов (по умолчанию 5)
        date_from: Дата первой подачи от YYYY-MM-DD включительно (UTC); без неё — с 1991-01-01, если задана date_to.
        date_to: Дата первой подачи до YYYY-MM-DD включительно (UTC); без неё — по сегодня, если задана date_from.
            Одинаковые границы выбирают один день. Без обеих дат фильтра нет.
    """
    return _search_arxiv(author_name, "author", max_results, date_from, date_to)


@mcp.tool()
def search_recent(
    topic: str,
    max_results: int = 5,
    date_from: str | None = None,
    date_to: str | None = None,
) -> str:
    """
    Поиск недавних статей по теме, отсортированных по дате первой подачи.
    Без дат возвращает последние статьи без ограничения давности.
    
    Args:
        topic: Тема для поиска (на английском языке)
        max_results: Максимальное количество результатов (по умолчанию 5)
        date_from: Дата первой подачи от YYYY-MM-DD включительно (UTC); без неё — с 1991-01-01, если задана date_to.
        date_to: Дата первой подачи до YYYY-MM-DD включительно (UTC); без неё — по сегодня, если задана date_from.
            Одинаковые границы выбирают один день. Без обеих дат фильтра нет.
    """
    try:
        search_query = _build_search_query(f"all:{topic}", date_from, date_to)
    except ValueError as e:
        return f"Ошибка в параметрах поиска: {e}"
    
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=15)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            return f"Статьи по теме '{topic}' не найдены."
        
        results = []
        for i, entry in enumerate(feed.entries, 1):
            arxiv_id = entry.id.split('/abs/')[-1]
            authors = ', '.join(a.name for a in entry.authors[:2])
            if len(entry.authors) > 2:
                authors += " и др."
            
            # Дата публикации
            published = entry.published[:10] if entry.published else "N/A"
            
            summary = entry.summary.replace('\n', ' ')[:200]
            
            results.append(
                f"{i}. [{published}] **{entry.title}**\n"
                f"   - ID: {arxiv_id} | Авторы: {authors}\n"
                f"   - {summary}...\n"
            )
        
        return f"Недавние статьи по теме '{topic}':\n\n" + "\n".join(results)
    
    except Exception as e:
        return f"Ошибка при запросе к arXiv: {str(e)}"


if __name__ == "__main__":
    print("📚 Запуск arXiv MCP Server...")
    print(f"📡 Сервер доступен по адресу: http://{ARXIV_HOST}:{ARXIV_PORT}/sse")
    print("⚠️  Для остановки нажмите Ctrl+C")
    print("")
    print("Доступные инструменты:")
    print("  • search_arxiv(query, field, max_results) — поиск статей")
    print("  • get_paper_details(arxiv_id) — детали статьи")
    print("  • search_by_author(author_name) — статьи автора")
    print("  • search_recent(topic) — недавние статьи")
    
    # SSE транспорт для совместимости с Responses API
    mcp.run(transport="sse", host=ARXIV_HOST, port=ARXIV_PORT)

