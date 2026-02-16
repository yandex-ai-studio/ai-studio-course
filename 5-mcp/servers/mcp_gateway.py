"""
MCP Gateway — объединённый MCP-сервер.

Автоматически сканирует текущую директорию на наличие .py файлов
с MCP-серверами и регистрирует все их инструменты под единым сервером.
Имена инструментов получают префикс из имени исходного сервера,
чтобы избежать конфликтов имён.

Запуск:
    python mcp_gateway.py

Переменные окружения:
    GATEWAY_HOST — хост (по умолчанию 0.0.0.0)
    GATEWAY_PORT — порт (по умолчанию 8000)
"""

from __future__ import annotations

import importlib
import inspect
import os
import re
import sys
from pathlib import Path
from types import ModuleType

from mcp.server.fastmcp import FastMCP

GATEWAY_FILENAME = Path(__file__).name

gateway = FastMCP("MCP Gateway")


# ── Вспомогательные функции ──────────────────────────────────────────────


def _find_mcp_instance(module: ModuleType) -> FastMCP | None:
    """Найти экземпляр FastMCP внутри импортированного модуля.

    Проверяет все атрибуты модуля и возвращает первый найденный
    объект типа FastMCP.  Если экземпляр не найден, возвращает None.
    """
    for _name, obj in inspect.getmembers(module):
        if isinstance(obj, FastMCP):
            return obj
    return None


def _derive_prefix(server_name: str) -> str:
    """Получить из имени сервера корректный префикс для инструмента.

    Пример: ``"ArxivResearch"`` → ``"arxivresearch"``,
            ``"MCP-сервер для заметок"`` → ``"mcp_сервер_для_заметок"``.
    """
    prefix = server_name.strip().lower()
    prefix = re.sub(r"[\s\-]+", "_", prefix)
    # Оставляем буквы, цифры, подчёркивания (включая кириллицу)
    prefix = re.sub(r"[^\w]", "", prefix, flags=re.UNICODE)
    return prefix


def _get_tools(mcp_instance: FastMCP) -> dict:
    """Извлечь зарегистрированные инструменты из FastMCP-экземпляра.

    Пробует несколько вариантов внутреннего API, чтобы быть
    совместимым с разными версиями библиотеки.

    Returns:
        Словарь ``{tool_name: tool_object}``, или пустой словарь.
    """
    # mcp (>=1.x)  — _tool_manager._tools
    mgr = getattr(mcp_instance, "_tool_manager", None)
    if mgr is not None:
        tools = getattr(mgr, "_tools", None)
        if tools:
            return dict(tools)

    # Альтернативный вариант — _tools напрямую
    tools = getattr(mcp_instance, "_tools", None)
    if tools:
        return dict(tools)

    return {}


# ── Обнаружение и регистрация ────────────────────────────────────────────


def _discover_and_register() -> list[tuple[str, str]]:
    """Просканировать директорию, найти MCP-серверы и зарегистрировать их инструменты.

    Returns:
        Список кортежей ``(prefixed_tool_name, source_server_name)``
        для каждого успешно зарегистрированного инструмента.
    """
    servers_dir = Path(__file__).parent.resolve()

    # Добавляем директорию в sys.path для корректного импорта
    if str(servers_dir) not in sys.path:
        sys.path.insert(0, str(servers_dir))

    py_files = sorted(servers_dir.glob("*.py"))
    registered: list[tuple[str, str]] = []

    for py_file in py_files:
        if py_file.name in (GATEWAY_FILENAME, "__init__.py"):
            continue

        module_name = py_file.stem

        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            print(f"⚠️  Не удалось импортировать {py_file.name}: {exc}")
            continue

        mcp_instance = _find_mcp_instance(module)
        if mcp_instance is None:
            print(f"ℹ️  {py_file.name}: FastMCP-экземпляр не найден, пропуск")
            continue

        server_name: str = getattr(mcp_instance, "name", module_name)
        prefix = _derive_prefix(server_name)
        tools = _get_tools(mcp_instance)

        if not tools:
            print(f"ℹ️  {py_file.name} ({server_name}): инструменты не найдены")
            continue

        for tool_name, tool_obj in tools.items():
            prefixed_name = f"{prefix}__{tool_name}"

            # Получаем оригинальную функцию
            fn = getattr(tool_obj, "fn", tool_obj)
            description = getattr(tool_obj, "description", "") or ""

            # Добавляем информацию об источнике в описание
            full_description = (
                f"[{server_name}] {description}" if description else f"[{server_name}]"
            )

            gateway.tool(name=prefixed_name, description=full_description)(fn)
            registered.append((prefixed_name, server_name))

    return registered


registered = _discover_and_register()


# ── Точка входа ──────────────────────────────────────────────────────────


def main() -> None:
    print("🚀 Запуск MCP Gateway...")
    print(f"📦 Зарегистрировано инструментов: {len(registered)}\n")
    for tool_name, server in registered:
        print(f"  • {tool_name}  (из {server})")
    print()

    host = os.getenv("GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("GATEWAY_PORT", "8000"))
    gateway.run(transport="streamable-http", host=host, port=port)


if __name__ == "__main__":
    main()
