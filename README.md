# MARVEL Chronology

Этот проект представляет собой веб-приложение, созданное для любителей комиксов Marvel, позволяющее пользователям удобно отслеживать и просматривать фильмы и сериалы в правильной хронологической последовательности. Приложение помогает пользователям определить порядок, в котором они должны смотреть различные произведения Marvel, и предоставляет функции для управления списком просмотренных фильмов.

#### Основные функции:

- Хронология фильмов и сериалов Marvel: Пользователи могут ознакомиться с полным списком фильмов и сериалов Marvel, отслеживая правильный порядок их просмотра.
- Регистрация и аутентификация: Пользователи могут зарегистрироваться и входить в систему, а также восстанавливать пароли через электронную почту, что обеспечивает безопасность и доступность аккаунтов.
- Отметки просмотренных фильмов: Удобная функция для отметки фильмов и сериалов, которые пользователь уже посмотрел. Это позволяет эффективно контролировать прогресс просмотра.
- Шкала прогресса: Пользователи могут видеть свою шкалу прогресса, что делает процесс просмотра более наглядным и интересным.

#### Технологии и решения:

1. Кэширование с помощью Redis: Запрашиваемые данные кэшируются для быстрого доступа. При добавлении нового элемента весь кэш обновляется, что позволяет сразу видеть изменения на сайте. Также предусмотрены механизмы для обновления кэша при удалении и изменении данных.

2. TrigramSimilarity: Реализован поиск по названиям фильмов с использованием триграммного сравнения, что позволяет пользователям находить фильмы по частичному совпадению.

3. Панель администратора: Организована структура записей с возможностью поиска, что позволяет администраторам управлять данными о фильмах и пользователях.

4. OpenAPI и Redoc: Использованы для документирования API, что упрощает взаимодействие с ним и его использование сторонними разработчиками.

5. Покрытие кода тестами: Все функции приложения покрыты тестами на 100%, что обеспечивает высокое качество кода и снижает вероятность ошибок.

6. Sitemap: Создана карта сайта для улучшения SEO, что позволяет поисковым системам качественно индексировать страницы вашего сайта.

7. Индексы: Установлены индексы на поля с русскими и английскими названиями фильмов, что значительно ускоряет поиск и фильтрацию записей.

## Table of Contents

- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Testing](#testing)

## Technologies

- Python 3.12.3
- Django 5.1.7
- PostgreSQL 17.0
- Redis 7.0.15

## Installation

1. Clone the repository
    ```
    git@github.com:hiOganes/marvel_chronology.git
    ```

2. Create and activate a virtual environment
    ```
    python -m venv venv
   
    source venv/bin/activate # for linux
    venv\Scripts\activate # for Windows
    ```

3. Install dependencies
    ```
    pip install -r requirements.txt
    ```

4. Get secret key to save to `.env` file
    ```
    python manage.py shell
   
    from django.core.management.utils import get_random_secret_key
   
    get_random_secret_key()
    ```

5. Create a `.env` file and configure environment variables
    ```
   # Main
    DEBUG=True
    SECRET_KEY='your-secret-key'
    ALLOWED_HOSTS=[]
   
   # PastgreSQL
    DB_NAME="your_db-name"
    DB_USER="your_user_db-name"
    DB_PASSWORD="your_user_db-password"
    DB_HOST="your_host_name"
    DB_PORT="port_psql"
   
   # Send Email
    EMAIL_HOST_USER="your email"
    EMAIL_HOST_PASSWORD="your password"
    ```

## Configuration

1. Apply database migrations
    ```
    python manage.py migrate
    ```

## Running the Project

1. Start the development server
    ```
    python manage.py runserver
    ```

2. Open your browser and go to [Website](http://127.0.0.1:8000/movies/list/)
3. Open your browser and go to [OpenAPI](http://127.0.0.1:8000/api/schema/swagger-ui/)

## Testing

 ```
   python manage.py loaddata fixtures/db_orders.json # Loading data into the database
   
   python manage.py test # Run tests
   ```