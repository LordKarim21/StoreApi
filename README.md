# Store Server

The project for study Django.

#### Stack:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   python3.9 -m venv ../venv
   source ../venv/bin/activate
   ```
   
2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
3. Run project dependencies, migrations, fill the database with the fixture data etc.:
   ```bash
   ./manage.py migrate
   ./manage.py loaddata <path_to_fixture_files>
   ./manage.py runserver 
   ```
   
4. Run [Redis Server](https://redis.io/docs/getting-started/installation/):
   ```bash
   redis-server
   ```
   
5. Run Celery:
   ```bash
   celery -A store worker --loglevel=INFO
   ```
   


# Store API

Данный проект представляет собой RESTful API для управления информацией о продуктах, пользователях и других сущностях в интернет-магазине.

## Установка

1. Склонируйте репозиторий на ваше устройство:

   ```bash
   git clone https://github.com/LordKarim21/StoreApi.git
   ```

2. Перейдите в директорию проекта:

   ```bash
   cd StoreApi
   ```

3. Создайте виртуальное окружение (опционально, но рекомендуется):

   ```bash
   python -m venv venv
   ```

4. Активируйте виртуальное окружение:

   - В Windows:

     ```bash
     venv\Scripts\activate
     ```

   - В macOS и Linux:

     ```bash
     source venv/bin/activate
     ```

5. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

6. Примените миграции:

   ```bash
   python manage.py migrate
   ```

7. Запустите локальный сервер:

   ```bash
   python manage.py runserver
   ```

Теперь ваше API будет доступно по адресу `http://127.0.0.1:8000/`.

## Использование

### Продукты

- `GET /api/product/`: Список всех продуктов.
- `GET /api/product/{id}/`: Информация о конкретном продукте.
- `POST /api/product/`: Создать новый продукт.
- `PUT /api/product/{id}/`: Обновить информацию о продукте.
- `DELETE /api/product/{id}/`: Удалить продукт.

### Теги

- `GET /api/tag/`: Список всех тегов.
- `GET /api/tag/{id}/`: Информация о конкретном теге.
- `POST /api/tag/`: Создать новый тег.
- `PUT /api/tag/{id}/`: Обновить информацию о теге.
- `DELETE /api/tag/{id}/`: Удалить тег.

### Категории

- `GET /api/categories/`: Список всех категорий.
- `GET /api/categories/{id}/`: Информация о конкретной категории.
- `POST /api/categories/`: Создать новую категорию.
- `PUT /api/categories/{id}/`: Обновить информацию о категории.
- `DELETE /api/categories/{id}/`: Удалить категорию.

### Акции

- `GET /api/sale/`: Список всех акций.
- `GET /api/sale/{id}/`: Информация о конкретной акции.
- `POST /api/sale/`: Создать новую акцию.
- `PUT /api/sale/{id}/`: Обновить информацию об акции.
- `DELETE /api/sale/{id}/`: Удалить акцию.

### Популярные продукты

- `GET /api/products/popular/`: Список популярных продуктов с рейтингом выше 4.5.

### Ограниченные продукты

- `GET /api/products/limited/`: Список продуктов с ограниченным количеством (больше 0).

...

Дополнительные URL-адреса и их описание можно найти в коде проекта.

## Кэширование

Код также поддерживает кэширование данных для оптимизации производительности. Для использования кэширования необходимо установить дополнительные зависимости, как описано выше.

## Вклад

Если вы обнаружили баги или хотите внести улучшения, не стесняйтесь создать Issue или Pull Request в репозитории.