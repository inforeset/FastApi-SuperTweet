# Начало
Проект: Сервис микроблогов
Разработан бэкенд для портала, который используется внутри компании.

## Used technology
* Python (3.10);
* FastApi (asynchronous Wev Framework);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* SQLAlchemy (working with database from Python);
* Alembic (database migrations made easy);
* Loguru (logging);
* Pytest (tests);

## Сборка докер-контейнеров
1. Необходимо скачать содержимое репозитория в отдельную папку.
2. Необходимо переименовать файл ".env.template" в ".env", при необходимости задать свои параметры.
3. В каталоге с файлом "docker-compose.yml" в терминале написать команду:
    ```
    docker-compose up -d
    ```

## Локальный запуск
1. Необходимо скачать содержимое репозитория в отдельную директорию.
2. Необходимо переименовать файл ".env.template" в ".env", при необходимости задать свои параметры.(не забудьте задать
параметры подключения к базе)
3. Необходимо установить Python версии 3.10, и создать виртуальное окружение, для этого в директории проекта в 
терминале написать команду:
    ```
    python -m venv venv
    ```
4. Чтобы начать пользоваться виртуальным окружением, необходимо его активировать:
    ```
    venv\Scripts\activate.bat - для Windows;
    source venv/bin/activate - для Linux и MacOS.
    ```
5. Необходимо установить все зависимости, для этого в директории проекта в терминале написать команду:
    ```
    pip install --no-cache-dir --upgrade -r requirements.txt
    ```
6. Необходимо применить миграции, для этого в консоли необходимо перейти в директорию "app" и в терминале написать 
команду:
    ```
    alembic upgrade head
    ```
7. В корневой директории проекта в терминале написать команду:
    ```
    uvicorn backend.api_v1.main:app --reload
    ```
8. Для запуска тестов необходимо перейти в директорию "app" и в терминале написать 
команду:
    ```
    pytest
    ```
### Работа
При запуске контейнеров, все миграции применятся автоматически, при ручном запуске необходимо применить миграции 
вручную так же добавляются пользователи со след. данными: 
1. логин "test1", api_key "test"
2. логин "test2", api_key "test2"
3. логин "test3", api_key "test3"
 
Пользователи test1 и test2 уже имет подписку друг на друга.

Доступ к документации по АПИ по адресу:
    ```
    <your_domain>/docs/
    ```