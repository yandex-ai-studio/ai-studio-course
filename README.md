# ai-studio-course
Курс по Yandex AI Studio для университетов

## Содержание курса


## Инструкции для преподавателей
1. Создайте файл `.env` с переменными `folder_id` и `api_key` вручную или сгенерируйте через `1-intro-ai-studio/Scripts/create_sa.bat` или `1-intro-ai-studio/Scripts/create_sa.sh`.
2. Загрузите `.env` на секретный URL, доступный вашим студентам.
3. Перед выдачей материалов студентам замените плейсхолдер в ноутбуках:
   ```bash
   python instructor/scripts/set-dotenv-url.py <URL_на_файл_env>
   ```
