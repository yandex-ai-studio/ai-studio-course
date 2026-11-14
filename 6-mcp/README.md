# Раздел 6: Model Context Protocol (MCP)

## Обзор

В этом разделе мы изучаем **Model Context Protocol (MCP)** — открытый стандарт для подключения LLM к внешним источникам данных и инструментам. Ключевое преимущество MCP в Responses API: **API сам подключается к MCP-серверу** и вызывает нужные функции, не требуя написания дополнительного клиентского кода. Мы рассматриваем развёртывание MCP-серверов, комбинирование MCP с локальными инструментами и использование нескольких MCP-серверов.

## Материалы

| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| 📖 | [MCP: Model Context Protocol][LectMCP] |  Удалённый вызов инструментов по протоколу MCP | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectMCP] |
| ✏️ | [ArxivResearchMCP.ipynb](ArxivResearchMCP.ipynb) | MCP для исследования научных статей: агент-исследователь, комбинирование MCP + Pydantic, несколько MCP-серверов | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/6-mcp/ArxivResearchMCP.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F6-mcp%2FArxivResearchMCP.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/6-mcp/ArxivResearchMCP.ipynb) |
| ✏️ | [MCP-сервера для работы с arXiv и medrXiv](servers) | Для запуска примера выше вам необходимо развернуть эти сервера на виртуальной машине (возможно, это уже сделано преподавателем) | |
| 🔬 | [MCPTravelLab.ipynb](Labs/MCPTravelLab.ipynb) | Туристический советник — агент с Web Search + погодным MCP-сервером на основе MCP Hub | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/6-mcp/Labs/MCPTravelLab.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F6-mcp%2FLabs%2FMCPTravelLab.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/6-mcp/Labs/MCPTravelLab.ipynb) |
| 🔬 | **Бонус-контент**: [TurtleMCPClient.ipynb](local-mcp/TurtleMCPClient.ipynb) | Рисование черепашкой через MCP — пример локального MCP-сервера. Требует локальной установки Python! | |

[LectMCP]: https://disk.yandex.ru/d/JENl9qPI6wCeXg

## Теоретический материал

### Что такое MCP

**[Model Context Protocol (MCP)](https://yandex.cloud/ru/docs/ai-studio/concepts/tools/mcp)** — это открытый стандарт, разработанный для стандартизации взаимодействия между LLM и внешними источниками данных и инструментами. MCP решает ту же задачу, что и Function Calling — расширяет возможности модели за счёт внешних функций — но при этом сам код инструментов выполняется на удалённом сервере, и там же содержатся описания инструментов. Нам достаточно лишь передать LLM ссылку на MCP-сервер, чтобы она сама "подключилась" к нему, загрузила список инструментов и начала их использовать.

Если при Function Calling клиент (ваш код) должен самостоятельно выполнять функции и передавать результаты модели, то при MCP эта работа полностью переносится в облако. Responses API **сам подключается к MCP-серверу**, запрашивает список доступных инструментов, вызывает нужные функции и передаёт результаты модели.

### Архитектура MCP

Архитектура MCP включает три компонента:

1. **MCP-сервер** — внешний сервис, который реализует набор инструментов (функций) и предоставляет к ним доступ по стандартному протоколу. Сервер публикует список доступных функций и обрабатывает вызовы. MCP-серверы можно писать на Python с помощью библиотеки [fastmcp](https://github.com/jlowin/fastmcp).

2. **Responses API** — выступает в роли MCP-клиента. При получении запроса с MCP-инструментом API подключается к указанному серверу, получает список функций, передаёт их модели, а затем выполняет вызовы. Клиентский код вообще не участвует в вызове MCP-функций.

3. **Клиент** (ваш код) — просто указывает URL MCP-сервера в описании инструмента и получает готовый результат от Responses API.

### Определение MCP-инструмента

В Responses API MCP-инструмент описывается простым словарём:

```python
arxiv_mcp_tool = {
    "type": "mcp",
    "server_label": "arXiv-Research",
    "server_description": "Поиск научных статей на arXiv",
    "server_url": "http://your-server:8000/sse",
    "require_approval": "never"
}
```

Ключевые параметры:
- **`server_label`** — метка сервера для идентификации в логах и ответах.
- **`server_description`** — описание, помогающее модели понять назначение сервера.
- **`server_url`** — URL для подключения (обычно с протоколом SSE или Streamable HTTP).
- **`require_approval`** — нужно ли запрашивать подтверждение у клиента перед вызовом функции (`"never"`, `"always"`, или список функций).

### Развёртывание MCP-серверов

Существуют два основных способа размещения MCP-серверов:

#### Виртуальная машина Yandex Cloud

MCP-сервер запускается как Python-процесс на [виртуальной машине](https://yandex.cloud/ru/docs/compute/) Yandex Cloud. Этот подход даёт полный контроль над сервером: выбор библиотек, управление ресурсами, логирование. Сервер должен быть доступен из интернета по указанному URL.

#### MCP Hub в Yandex Cloud

[MCP Hub](https://yandex.cloud/ru/docs/functions/concepts/mcp-server) — управляемый сервис в Yandex Cloud, который позволяет создавать MCP-серверы без управления инфраструктурой. MCP Hub поддерживает несколько способов создания инструментов, из которых мы рассмотрим два:

1. **REST API** — инструмент описывается декларативно и проксирует вызовы к существующему HTTP API.
2. **Cloud Functions** — инструмент реализуется как [облачная функция](https://yandex.cloud/ru/docs/functions/), которая автоматически масштабируется и не требует управления серверами.

MCP Hub особенно удобен, когда нужно быстро подключить существующее API как инструмент для LLM без написания полноценного MCP-сервера.

### Комбинирование MCP с локальными инструментами

Одна из ключевых возможностей — **одновременное использование MCP-инструментов и локальных Pydantic-функций** в одном агенте. Класс `Agent` поддерживает смешанный список инструментов:

```python
agent = Agent(
    client, model=model,
    instruction="...",
    tools=[arxiv_mcp_tool, SaveNote]  # MCP + Pydantic
)
```

Responses API автоматически разводит вызовы: MCP-функции выполняются в облаке, а Pydantic-функции — локально на стороне клиента. Модель видит все инструменты одновременно и может выбирать наиболее подходящий для каждого шага.

### Несколько MCP-серверов

В одном агенте можно подключить **несколько MCP-серверов одновременно**. Каждый сервер описывается отдельным словарём с уникальным `server_label`, и модель получает инструменты со всех серверов. Это позволяет строить сложные агентские системы: например, использовать один сервер для поиска научных статей, другой для сохранения заметок, а третий для обращения к корпоративной базе данных.

Поскольку MCP-серверы доступны по сети, **разные агенты могут использовать одни и те же серверы** — например, агент-исследователь сохраняет заметки в MCP-сервер, а агент-писатель читает их оттуда для создания отчёта. Это открывает возможности для построения распределённых многоагентных систем, в которых информация передаётся между агентами через общие инструменты.

## MCP-серверы

Для работы примеров потребуется развернуть и запустить несколько MCP-серверов на виртуальной машине. В директории [`servers/`](servers/) находятся реализации MCP-серверов, используемых в курсе:

| Файл | Описание |
|------|----------|
| [`arxiv_mcp.py`](servers/arxiv_mcp.py) | Поиск и получение научных статей с arXiv |
| [`medrxiv_mcp.py`](servers/medrxiv_mcp.py) | Поиск медицинских препринтов на medRxiv |
| [`notes.py`](servers/notes.py) | Сохранение и управление личными заметками |
| [`mcp_gateway.py`](servers/mcp_gateway.py) | Маршрутизатор для запуска нескольких MCP-серверов |

[Подробнее про запуск MCP-серверов](servers/README.md)

## Практические работы

### 🔬 MCPTravelLab.ipynb

Создайте идеального ИИ-советника по путешествиям, который всегда в курсе событий! Ваша задача в этой лабораторной работе — создать умного агента, который дает персонализированные рекомендации по путешествиям, комбинируя поиск в реальном времени в интернете со специализированным погодным сервисом. Вы подключите своего агента к погодному инструменту через протокол Model Context Protocol (MCP), что позволит ему получать актуальные прогнозы для любого направления в мире.



## Предварительные требования

- Выполненные разделы 1-4
- Библиотеки: `openai`, `python-dotenv`, `fastmcp`
- Для MCP-серверов: `feedparser`, `requests`, `fastmcp`
