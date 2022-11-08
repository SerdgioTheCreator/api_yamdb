## API_YAMDB

**API** (от англ. **A**pplication **P**rogramming **I**nterface, «программный интерфейс
приложения») — это интерфейс для обмена данными.

>Предназначен для взаимодействия frontend и backend составляющей
> приложения **Yamdb**. С его помощью можно:

- Зарегистрировать нового пользователя
- Получить JWT-токен
- Добавить нового пользователя
- Получить список всех пользователей
- Получить/изменить данные своей учетной записи
- Получить/удалить пользователя по username
- Изменить данные пользователя по username
- Добавить/удалить категорию(*тип*) произведения, получить список всех категорий
- Добавить/удалить жанр произведения, получить список всех жанров
- Добавить новое произведение
- Получить список всех произведений
- Получить/обновить/удалить произведение по id
- Добавить новый отзыв
- Получить список всех отзывов
- Получить/обновить/удалить отзыв по id
- Добавить новый комментарий для отзыва
- Получить список всех комментариев к отзыву по id
- Получить/обновить/удалить комментарий к отзыву по id

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SerdgioTheCreator/api_yamdb
```

```
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Открыть документацию:

```
http://127.0.0.1:8000/redoc/
```

### Пример запросов:

Регистрация нового пользователя:

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}
```

Получение JWT-токена:

```
http://127.0.0.1:8000/api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

Добавление новой категории:

```
http://127.0.0.1:8000/api/v1/categories/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Добавление жанра:

```
http://127.0.0.1:8000/api/v1/genres/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Добавление произведения:

```
http://127.0.0.1:8000/api/v1/titles/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Добавление нового отзыва:

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

```json
{
  "text": "string",
  "score": 1
}
```

Добавление комментария к отзыву:

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

```json
{
  "text": "string"
}
```

Добавление пользователя:

```
http://127.0.0.1:8000/api/v1/users/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Импорт из csv файла выполняется командой:

```
python manage.py runscript import
```


### Авторы: Коновалов Сергей, Акимов Максим, Бобров Сергей, команда ЯндексПрактикум
