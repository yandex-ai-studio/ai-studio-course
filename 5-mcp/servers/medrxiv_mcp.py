"""
medRxiv MCP Server
MCP-сервер для поиска препринтов на medRxiv.

Запуск:
    python medrxiv_mcp.py

Сервер будет доступен по адресу: http://localhost:8001/sse
"""

import requests
from mcp.server.fastmcp import FastMCP

# Создаём MCP сервер
mcp = FastMCP("MedRxivResearch")

# API URL
API_URL = "https://api.biorxiv.org/details/medrxiv"

@mcp.tool()
def search_medrxiv(interval: str = "2024-01-01/2025-01-01", cursor: int = 0) -> str:
    """
    Получает список препринтов с medRxiv за указанный интервал.
    
    Args:
        interval: Интервал дат в формате YYYY-MM-DD/YYYY-MM-DD
        cursor: Смещение для пагинации (по умолчанию 0)
    """
    url = f"{API_URL}/{interval}/{cursor}"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        
        if 'collection' not in data or not data['collection']:
            return "Статьи не найдены."
            
        results = []
        for i, paper in enumerate(data['collection'], 1):
            results.append(
                f"{i}. **{paper['title']}**\n"
                f"   - DOI: {paper['doi']}\n"
                f"   - Авторы: {paper['authors']}\n"
                f"   - Дата: {paper['date']}\n"
                f"   - Аннотация: {paper['abstract'][:200]}...\n"
            )
            if i >= 5: break # Ограничим 5 результатами для примера
            
        return "\n".join(results)
    except Exception as e:
        return f"Ошибка при запросе к medRxiv: {str(e)}"

if __name__ == "__main__":
    print("🏥 Запуск medRxiv MCP Server...")
    print("📡 Сервер доступен по адресу: http://localhost:8001/sse")
    
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8001
    )
