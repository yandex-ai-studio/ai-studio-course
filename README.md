# Yandex AI Studio: курс для университетов

## Аннотация

В последние годы фундаментальные ИИ-модели совершили прорыв в множестве областей, от человеко-машинного взаимодействия до обработки неструктурированных данных. В этом курсе мы осваиваем доступные в Yandex AI Studio сервисы по работе с LLM и другими сервисами.

Мы увидим, как эффективно использовать языковые модели для извлечения данных из текстов, для общения с пользователем, взаимодействия с внешними сервисами и организации Deep Research. Курс содержит множество примеров использования LLM в задачах, релевантных науке и образованию.

Курс предназначен для преподавателей, которые хотят внедрить практические примеры использования LLM в свои курсы, либо поставить отдельный курс по созданию многоагентных систем на базе современного облачного инструмента. Студенты могут использовать курс для само-образования, поскольку он содержит все необходимые материалы и задания для самостоятельного выполнения.

> Для преподавателей доступны также решения всех практических заданий. Чтобы у студентов не было доступа к готовым решениям, все такие файлы (с суффиксом `-Solution`) зашифрованы с помощью [`git-crypt`](https://github.com/AGWA/git-crypt). Чтобы посмотреть эти файлы, необходимо получить ключ преподавателя.

## Содержание курса

Курс содержит следующие материалы:

📖 — слайды лекций (Powerpoint)<br/>
✏️ — Jupyter Notebooks с лекциями<br/> 
🔬 — Jupyter Notebooks с лабораторными работами


| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| **1** | **[Введение в Yandex AI Studio](1-intro-ai-studio/)** | | |
| 📖 | [AI Studio и Yandex Cloud][LectAIStudio] | Основные концепции Yandex Cloud и вызов API через Yandex AI Studio SDK и Responses API | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectAIStudio]
| ✏️ | [CloudConnect.ipynb](1-intro-ai-studio/CloudConnect.ipynb) | Подключение к Yandex Cloud, работа с YandexGPT, YandexART и введение в Responses API | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/1-intro-ai-studio/CloudConnect.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F1-intro-ai-studio%2FCloudConnect.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/1-intro-ai-studio/CloudConnect.ipynb) |
| 🔬 | [LLMTalk.ipynb](1-intro-ai-studio/Labs/LLMTalk.ipynb) | Две LLM общаются друг с другом — создание класса `Agent` и диалог между двумя LLM | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/1-intro-ai-studio/Labs/LLMTalk.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F1-intro-ai-studio%2FLabs%2FLLMTalk.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/1-intro-ai-studio/Labs/LLMTalk.ipynb) |
| **2** | **[Responses API](2-responses-api/)** | | |
| 📖 | [Вызов LLM через Responses API][LectRespAPI] | Изучаем, как использовать Reponses API для поддержания контекста диалога, формирования структурного ответа и работы с мультимодальными моделями | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectRespAPI]
| ✏️ | [ResponsesAPI.ipynb](2-responses-api/ResponsesAPI.ipynb) | Responses API: диалоговый контекст, структурированный вывод (Pydantic, JSON mode), визуализация данных и мультимодальные модели | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/2-responses-api/ResponsesAPI.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F2-responses-api%2FResponsesAPI.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/2-responses-api/ResponsesAPI.ipynb) |
| 🔬 | [PaperSummarize.ipynb](2-responses-api/Labs/PaperSummarize.ipynb) | Суммаризация научной статьи — извлечение ключевой информации из текста | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/2-responses-api/Labs/PaperSummarize.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F2-responses-api%2FLabs%2FPaperSummarize.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/2-responses-api/Labs/PaperSummarize.ipynb) |
| 🔬 | [AgenticImageGeneraton.ipynb](2-responses-api/Labs/AgenticImageGeneraton.ipynb) | Агентный цикл генерации изображений — итеративная генерация и улучшение изображений с помощью LLM | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/2-responses-api/Labs/AgenticImageGeneraton.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F2-responses-api%2FLabs%2FAgenticImageGeneraton.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/2-responses-api/Labs/AgenticImageGeneraton.ipynb) |
| **3** | **[Function Calling](3-tool-calling/)** | | |
| 📖 | [Вызов инструментов][LectFunctionCalling] | Изучаем, как можно расширить LLM дополнительными инструментами, и как упростить реализацию с помощью pydantic | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectFunctionCalling]
| ✏️ | [ToolCalling.ipynb](3-tool-calling/ToolCalling.ipynb) | Основы Function Calling на примере калькулятора: работа с JSON Schema и Pydantic | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/ToolCalling.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FToolCalling.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/ToolCalling.ipynb) |
| ✏️ | [ArxivResearch.ipynb](3-tool-calling/ArxivResearch.ipynb) | Исследовательский агент для arXiv: поиск статей, Pydantic-инструменты, веб-поиск | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/ArxivResearch.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FArxivResearch.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/ArxivResearch.ipynb) |
| 🔬 | [GrapherTool.ipynb](3-tool-calling/Labs/GrapherTool.ipynb) | Агент-аналитик с построением графиков — создание агента, который строит графики по запросу и извлекает данные из текста | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/Labs/GrapherTool.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FLabs%2FGrapherTool.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/Labs/GrapherTool.ipynb) |
| 🔬 | [AgentDrawing.ipynb](3-tool-calling/Labs/AgentDrawing.ipynb) | Агент-художник с Turtle Graphics — управление черепашкой через Function Calling | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/3-tool-calling/Labs/AgentDrawing.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F3-tool-calling%2FLabs%2FAgentDrawing.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/3-tool-calling/Labs/AgentDrawing.ipynb) |
| **4** | **[RAG и поиск](4-rag-search/)** | | |
| 📖 | [Файловый поиск (RAG) и веб-поиск][LectSearch] | Учимся расширять модели с помощью втроенных в Responses API инструментов поиска | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectSearch]
| ✏️ | [WebSearch.ipynb](4-rag-search/WebSearch.ipynb) | Web Search: поиск в интернете, суммаризация новостей, конкурентный анализ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/4-rag-search/WebSearch.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F4-rag-search%2FWebSearch.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/4-rag-search/WebSearch.ipynb) |
| ✏️ | [FileSearch.ipynb](4-rag-search/FileSearch.ipynb) | File Search: создание базы знаний из файлов, Vector Store, Telegram-бот | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/4-rag-search/FileSearch.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F4-rag-search%2FFileSearch.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/4-rag-search/FileSearch.ipynb) |
| 🔬 | [OpenAlexLab.ipynb](4-rag-search/Labs/OpenAlexLab.ipynb) | RAG vs Tool Calling — сравнение подходов на базе подмножества научных статей из OpenAlex | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/4-rag-search/Labs/OpenAlexLab.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F4-rag-search%2FLabs%2FOpenAlexLab.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/4-rag-search/Labs/OpenAlexLab.ipynb) |
| **5** | **[Дополнительные встроенные инструменты](5-other-int-tools/)** | | |
| ✏️ | [CodeInterpreter.ipynb](5-other-int-tools/CodeInterpreter.ipynb) | Code Interpreter: выполнение Python-кода, работа с файлами в контейнере, pandas и визуализация данных | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/5-other-int-tools/CodeInterpreter.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F5-other-int-tools%2FCodeInterpreter.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/5-other-int-tools/CodeInterpreter.ipynb) |
| ✏️ | [ImageGeneration.ipynb](5-other-int-tools/ImageGeneration.ipynb) | Image Generation Tool: агентная генерация и итеративное улучшение изображений с Qwen3.6 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/5-other-int-tools/ImageGeneration.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F5-other-int-tools%2FImageGeneration.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/5-other-int-tools/ImageGeneration.ipynb) |
| 🔬 | [DataAnalysis-Solution.ipynb](5-other-int-tools/Labs/DataAnalysis-Solution.ipynb) | Анализ рынка труда с помощью Code Interpreter — полное решение лабораторной работы | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/5-other-int-tools/Labs/DataAnalysis-Solution.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F5-other-int-tools%2FLabs%2FDataAnalysis-Solution.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/5-other-int-tools/Labs/DataAnalysis-Solution.ipynb) |
| **6** | **[Model Context Protocol (MCP)](6-mcp/)** | | |
| 📖 | [MCP: Model Context Protocol][LectMCP] |  Удалённый вызов инструментов по протоколу MCP | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectMCP]
| ✏️ | [ArxivResearchMCP.ipynb](6-mcp/ArxivResearchMCP.ipynb) | MCP для исследования научных статей: агент-исследователь, комбинирование MCP + Pydantic, несколько MCP-серверов | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/6-mcp/ArxivResearchMCP.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F6-mcp%2FArxivResearchMCP.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/6-mcp/ArxivResearchMCP.ipynb) |
| ✏️ | [MCP-сервера для работы с arXiv и medrXiv](6-mcp/servers) | Для запуска примера выше вам необходимо развернуть эти сервера на виртуальной машине (возможно, это уже сделано преподавателем) | |
| 🔬 | [MCPTravelLab.ipynb](6-mcp/Labs/MCPTravelLab.ipynb) | Туристический советник — агент с Web Search + погодным MCP-сервером на основе MCP Hub | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/6-mcp/Labs/MCPTravelLab.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F6-mcp%2FLabs%2FMCPTravelLab.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/6-mcp/Labs/MCPTravelLab.ipynb) |
| 🔬 | **Бонус-контент**: [TurtleMCPClient.ipynb](6-mcp/local-mcp/TurtleMCPClient.ipynb) | Рисование черепашкой через MCP — пример локального MCP-сервера. Требует локальной установки Python! | |
| **7** | **[Многоагентные системы](7-multiagent/)** | | |
| 📖 | [Агенты и многоагентные системы][LectAgents] |  Говорим про агентный цикл, планирование и ReAct-агентов, а также как и зачем комбинировать агентов в многоагентную систему | [![PPTX](https://img.shields.io/badge/PPTX-red.svg)][LectAgents]
| ✏️ | [DeepResearch.ipynb](7-multiagent/DeepResearch.ipynb) | Deep Research Agent: агентский цикл, RunHooks, Streaming, три паттерна многоагентной координации | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/7-multiagent/DeepResearch.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F7-multiagent%2FDeepResearch.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/7-multiagent/DeepResearch.ipynb) |
| 🔬 | [DeepResearchLab.ipynb](7-multiagent/Labs/DeepResearchLab.ipynb) | Medical Deep Research Agent — многоагентная система с MCP-серверами и генерацией PDF-отчёта | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/7-multiagent/Labs/DeepResearchLab.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F7-multiagent%2FLabs%2FDeepResearchLab.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/7-multiagent/Labs/DeepResearchLab.ipynb) |
| **8** | **[SpeechKit и Vision OCR](8-other-services/)** | | |
| ✏️ | [SpeechKit.ipynb](8-other-services/SpeechKit.ipynb) | SpeechKit TTS/STT: синтез коротких сообщений, радиопередача с разными голосами и распознавание результата | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/SpeechKit.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FSpeechKit.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/SpeechKit.ipynb) |
| ✏️ | [LongSpeech.ipynb](8-other-services/LongSpeech.ipynb) | Длинное аудио: распознавание подкаста, speaker labeling и обратный синтез с разными голосами | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/LongSpeech.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FLongSpeech.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/LongSpeech.ipynb) |
| ✏️ | [OCR.ipynb](8-other-services/OCR.ipynb) | Vision OCR, мультимодальная Qwen3.6, перевод текста и наложение перевода поверх изображения | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/OCR.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FOCR.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/OCR.ipynb) |
| 🔬 | [LectureRAG.ipynb](8-other-services/Labs/LectureRAG.ipynb) | RAG-ассистент по лекции: PDF-слайды, OCR, VLM-описания, транскрипт аудио и File Search | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/Labs/LectureRAG.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FLabs%2FLectureRAG.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/Labs/LectureRAG.ipynb) |

[LectAIStudio]: https://disk.yandex.ru/i/tUgkFRO7XAkiOQ
[LectRespAPI]: https://disk.yandex.ru/i/yRGTadYhxkmb5Q
[LectFunctionCalling]: https://disk.yandex.ru/d/ouAHZ-tAkJ1LLA
[LectSearch]: https://disk.yandex.ru/d/_ji2zdWwYiRQgg
[LectMCP]: https://disk.yandex.ru/d/JENl9qPI6wCeXg
[LectAgents]: https://disk.yandex.ru/d/SXlgGWa685WyRQ

## Что нужно для обучения

### Среда для выполнения Jupyter

Большинство обучающих примеров оформлены в виде Jupyter Notebook-ов. Для их запуска существует несколько вариантов:

* Установить окружение Python себе на компьютер. Опционально можно также установить Visual Studio Code с соответствующими расширениями. [Инструкция](https://soshnikov.com/education/how-to-execute-notebooks-from-github-ru)
* Использовать облачные сервисы [Google Colab](https://colab.research.google.com) или [Binder](https://mybinder.org).
* Если у вас есть доступ в Yandex Cloud - использовать Yandex Datasphere.

> Ссылки на открытие всех материалов курса в Colab / Binder / Datasphere есть в табличке материалов выше. 

### Доступ в облако

Для обучения вам также потребуется программный доступ к Yandex AI Studio или облаку Yandex Cloud, а для некоторых разделов - доступ к веб-консоли облака.

#### Ключи для доступа к облачным сервисам

В большинстве примеров и лабораторных работ по курсу мы будем работать с облачными сервисами через API. Для вызова облачных сервисов нам необходимо знать:

* `folder_id` - идентификатор облачного каталога
* `api_key` - ключ для доступа к облачным сервисам

В большинстве примеров мы предполагаем, что эти значения хранятся в специальном файле `.env`, который скачивается в начале работы или руками помещается в текущую директорию. Если вы работаете локально на своём компьютере - вы также можете вручную поместить эти значения в переменные окружения.

Если вы получили эти ключи от преподавателя, или в выданных вам материалах уже прописан адрес для скачивания `.env`-файла - всё хорошо. Если у вас нет этих значений - читайте ниже.

#### Полный доступ к облачному аккаунту

В идеале, у вас должен быть полный доступ к облаку Yandex Cloud или AI Studio со своим Yandex ID. Возможны несколько вариантов получения такого доступа:

* Вы можете зарегистрировать новую учётную запись. Для новых клиентов доступен [пробный период](https://yandex.cloud/ru/docs/billing/concepts/trial-period)
* Иногда возможно получить учётную запись от университета или преподавателя в рамках курса

Имея доступ в облако/AI Studio, вы можете самостоятельно создать ключи `folder_id` и `api_key` - либо в веб-консоли, либо запустив один из скриптов [отсюда](1-intro-ai-studio/scripts/). 

### Рекомендованный порядок изучения материалов

Рекомендуется изучать разделы курса от начала и до конца. Перейдите по ссылке каждого раздела, чтобы углубиться в соответствующие материалы. Как правило, порядок изучения раздела такой:

* Смотрите презентацию
* В нужных местах (где в презентации есть отсылка на материалы) - запускаете демонстрационный Jupyter Notebook
* Выполняете лабораторные работы

## Инструкции для преподавателей

### Подключение студентов к Yandex Cloud

Задания и примеры, предлагаемые в рамках курса, требуют для подключения к облачным ресурсам лишь идентификатора каталога `folder_id` и API-ключа сервисного аккаунта `api_key`. Вы можете:

* Предоставить студентам доступ в AI Studio и возможность самим генерировать себе ключи
* Раздать студентам готовые значения `folder_id` и `api_key` 

Во втором случае, вы можете записать соответствующие значения в файл `.env` и загрузить его на некоторый секретный URL, доступный вашим студентам.

В ноутбуках используется такой код для загрузки файла:
```
!curl -o .env {{url_of_dotenv_file}}
```

Предполагается, что студенты самостоятельно заменят плейсхолдер в ноутбуках, но можно сделать это автоматически, и раздать студентам уже готовые ноутбуки со ссылкой на файл для авторизации. Для этого:

1. Создайте файл `.env` с переменными `folder_id` и `api_key` вручную или сгенерируйте через `1-intro-ai-studio/Scripts/create_sa.bat` или `1-intro-ai-studio/Scripts/create_sa.sh`.
2. Загрузите файл `.env` на некоторый секретный URL, доступный вашим студентам. Например, можно создать публично-доступный бакет в Yandex Cloud S3.
3. Перед выдачей материалов студентам замените плейсхолдер в ноутбуках, запустив скрипт:
   ```bash
   python instructor/scripts/set-dotenv-url.py <URL_на_файл_env>
   ```

> Если вы будете выкладывать соответствующие файлы на GitHub или в публичный доступ помните, что ссылка будет всем видна, и вашими ключами потенциально могут воспользоваться. Рекомендуется использовать ключи с краткосрочным временем жизни. 

### Решения лабораторных работ

В данном репозитории содержатся решения домашних задание и лабораторных работ - они имеют суффикс `-Solution`. При этом они зашифрованы с помощью утилиты [`git-crypt`](https://github.com/AGWA/git-crypt), чтобы у студентов не было доступа к готовым решениям. 

Чтобы посмотреть решения, неоходимо:

* Установить себе на компьютер [git-crypt](https://github.com/AGWA/git-crypt). Релиз для Linux и Windows можно скачать [здесь](https://github.com/AGWA/git-crypt/releases/tag/0.7.0), на Mac - [установить с помощью brew](https://www.geeksforgeeks.org/installation-guide/how-to-install-git-crypt-on-macos/).
* Получить ключ для преподавателя
* Выполнить на своём компьютере в репозитории курса команды:
  ```bash
  git-crypt unlock <path_to_keyfile>
  ```

Удачных занятий!

## Автор курса

Курс был подготовлен [Дмитрием Сошниковым](https://soshnikov.com/ru). Дмитрий является основным разработчиком [Microsoft AI for Beginners Curriculum](https://github.com/microsoft/ai-for-beginners), читает курс по Искусственному интеллекту в МАИ, является доцентом НИУ ВШЭ и техническим руководителем AI Lab Школы дизайна. Начал заниматься ИИ и многоагентными системами в 1995 году. Автор телеграм-канала [Облачный адвокат](http://t.me/shwarsico).
