# Notes

Cервис для создания, просмотра и удаления заметок на FastAPI.
У каждой заметки есть важность (priority 1–5), список можно сортировать.

## Установка

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt

## Запуск

    uvicorn app_final:app --host 0.0.0.0 --port 8000

Открыть http://localhost:8000/docs

## Запуск без --reload

    uvicorn app_final:app --host 0.0.0.0 --port 8000

## Тесты

    python -m pytest -v

## Переменные окружения

| Имя | По умолчанию |
| APP_VERSION | 1.0.0 |

Файл '.env.example' в репозитории.

## Маршруты

| Метод | Путь | Что делает |
| GET | / | приветствие |
| GET | /health | проверка |
| GET | /version | версия |
| GET | /notes | все заметки (?sort=priority / ?sort=-priority) |
| POST | /notes | создать заметку |
| GET | /notes/{id} | одна заметка |
| DELETE | /notes/{id} | удалить заметку |


## Проверка

    curl http://localhost:8000/health
    curl http://localhost:8000/version

## Логи

Пишутся в файл 'app.log' в корне проекта.

    cat app.log

## Диагностика

- /health вернул {"status":"ok"}.
- /version вернул версию из APP_VERSION.
- Ответ {"error":"Note not found"} — заметки с таким id нет.

## CI

GitHub Actions запускает тесты на push и pull request, после успешных тестов создаёт artifact 'app-files'.