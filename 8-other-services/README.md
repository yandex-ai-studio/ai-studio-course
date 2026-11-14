# Раздел 8: SpeechKit и Vision OCR

## Обзор

В этом разделе мы изучаем дополнительные AI-сервисы Yandex Cloud, которые хорошо дополняют языковые модели и агентные системы: **SpeechKit** для синтеза и распознавания речи, **Vision OCR** для извлечения текста из изображений и **Yandex Translate** для перевода. В качестве лабораторной работы мы собираем мультимодального RAG-ассистента по лекции: он использует слайды, OCR, описание изображений через VLM и транскрипт аудиозаписи.

## Материалы

| Тип | Материал | Описание | Запуск |
|:---:|----------|----------|:------:|
| ✏️ | [SpeechKit.ipynb](SpeechKit.ipynb) | TTS/STT для коротких сообщений: синтез фраз, радиопередача с разными голосами и распознавание результата | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/SpeechKit.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FSpeechKit.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/SpeechKit.ipynb) |
| ✏️ | [LongSpeech.ipynb](LongSpeech.ipynb) | Длинное аудио: распознавание подкаста, speaker labeling и обратный синтез с разными голосами | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/LongSpeech.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FLongSpeech.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/LongSpeech.ipynb) |
| ✏️ | [OCR.ipynb](OCR.ipynb) | Vision OCR, мультимодальная Qwen3.6, перевод текста и наложение перевода поверх изображения | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/OCR.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FOCR.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/OCR.ipynb) |
| 🔬 | [LectureRAG.ipynb](Labs/LectureRAG.ipynb) | RAG-ассистент по лекции: слайды PDF, OCR, VLM-описания, транскрипт аудио и File Search | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yandex-ai-studio/ai-studio-course/blob/main/8-other-services/Labs/LectureRAG.ipynb) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yandex-ai-studio/ai-studio-course/HEAD?urlpath=%2Fdoc%2Ftree%2F8-other-services%2FLabs%2FLectureRAG.ipynb) [![DataSphere](https://storage.yandexcloud.net/datasphere-assets/datasphere_badge_v2_ru.svg)](https://datasphere.yandex.cloud/import-ipynb?path=https://raw.githubusercontent.com/yandex-ai-studio/ai-studio-course/main/8-other-services/Labs/LectureRAG.ipynb) |

## Подготовка данных

В разделе используются несколько крупных файлов, которые хранятся за пределами GitHub-репозитория. Прежде, чем выполнять примеры кода из Jupyter-ноутбуков, скачайте необходимые данные командой `data\download.bat` (под Windows). Вы также можете использовать свои файлы с примерами, внеся соответствующие небольшие изменения в код.

## Теоретический материал

### SpeechKit: TTS и STT

**Yandex SpeechKit** — сервис для работы с речью. Он решает две базовые задачи:

* **Text-to-Speech (TTS)** — синтез речи из текста. TTS используется в голосовых ассистентах, аудиоуведомлениях, тренажёрах произношения, озвучке интерфейсов и генерации голосовых сообщений.
* **Speech-to-Text (STT)** — распознавание речи в текст. STT используется для голосового ввода, протоколирования встреч, транскрибации лекций, поиска по аудиоархивам и обработки голосовых сообщений.

В коротких сценариях, например в голосовом боте, обычно достаточно синхронного распознавания небольшого файла. Для длинных файлов удобнее использовать отложенные асинхронные операции: аудио отправляется на обработку, а результат забирается после завершения.

Документация:

* [Yandex SpeechKit](https://yandex.cloud/ru/docs/speechkit/)
* [SpeechKit в AI Studio SDK](https://aistudio.yandex.ru/docs/en/ai-studio/sdk-ref/types/speechkit.html)
* [Пример TTS в AI Studio SDK](https://github.com/yandex-cloud/yandex-ai-studio-sdk/blob/master/examples/sync/speechkit/text_to_speech/run_simple.py)
* [Пример STT в AI Studio SDK](https://github.com/yandex-cloud/yandex-ai-studio-sdk/blob/master/examples/sync/speechkit/speech_to_text/run_simple.py)

### Speaker labeling

**Speaker labeling** — это разметка аудио по говорящим. Сервис не сообщает имя человека, но старается разделить реплики на устойчивые метки вроде `speaker_0` и `speaker_1`. Это полезно для интервью, подкастов, совещаний и лекций с несколькими участниками: после распознавания можно строить диалоговую таблицу, суммаризировать вклад каждого участника или искать вопросы и ответы.

В ноутбуке `LongSpeech.ipynb` этот сценарий построен по образцу [speaker_labeling.py](https://github.com/yandex-cloud/yandex-ai-studio-sdk/blob/master/examples/sync/speechkit/speech_to_text/speaker_labeling.py), а обратный синтез длинного текста — по образцу [run_big_input.py](https://github.com/yandex-cloud/yandex-ai-studio-sdk/blob/master/examples/sync/speechkit/text_to_speech/run_big_input.py).

### Vision OCR и VLM

**Vision OCR** извлекает текст из изображений и документов. В отличие от простого “прочитать картинку”, OCR возвращает структурированный результат: полный текст, блоки, строки, слова и координаты. Координаты позволяют подсвечивать найденный текст, накладывать перевод или связывать найденный фрагмент с исходной областью изображения.

**VLM** (vision-language model) работает шире: модель получает изображение и текстовый запрос, а затем может описать изображение, объяснить диаграмму, выделить важные визуальные элементы или сравнить OCR-текст с тем, что видно на картинке. В разделе мы используем Qwen3.6 как мультимодальную модель через Responses API.

Документация:

* [Vision OCR](https://yandex.cloud/ru/docs/vision/concepts/ocr/)
* [Vision OCR API](https://yandex.cloud/en/docs/vision/ocr/api-ref/TextRecognition/recognize)
* [Yandex AI Studio](https://yandex.cloud/ru/docs/ai-studio/)

### Yandex Translate

**Yandex Translate** переводит массивы строк между языками. После OCR это особенно удобно: можно распознать иностранный текст на изображении, перевести строки по отдельности и затем наложить перевод обратно на исходную картинку. Такой конвейер превращает статичное изображение в простейший прототип визуального переводчика.

Документация:

* [Yandex Translate](https://yandex.cloud/ru/docs/translate/)
* [Translate API](https://yandex.cloud/en/docs/translate/api-ref/grpc/Translation/translate)

### Мультимодальный RAG

В лабораторной работе мы строим RAG-ассистента по лекции. Его база знаний содержит:

* OCR-текст со слайдов;
* VLM-описания слайдов и диаграмм;
* транскрипт аудиозаписи лекции;
* ссылку из каждого текстового файла на исходное изображение слайда.

Такой подход помогает не потерять визуальную информацию. Если студент задаёт вопрос, ассистент может найти релевантный текстовый фрагмент и одновременно показать исходный слайд, на котором была схема или диаграмма.
