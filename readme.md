# api-rshb-game

### Project setup

Скопировать .env.exemple в .env

Основные параметры:<br>
Раздел Django development config - настройки режима запуска<br>
DEVELOPMENT_MODE -> 'True' - основная база данных PostgresSQL, 'False" - SQLlite<br>

Раздел Django Superuser - данные для создания суперпользователя

Раздел Django Postgres Database Config - настройки Django Database

Раздел Postgres container config - переменные для Postgres Container

```
docker-compose up --build
```

