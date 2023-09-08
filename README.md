# Foodrgam

 Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на `Django` и `DjangoRestFramework`. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием `Redoc`.

## Особенности реализации

- Проект завернут в Docker-контейнеры;
- Образы foodgram_frontend и foodgram_backend запушены на DockerHub;
- Реализован workflow c автодеплоем на удаленный сервер и отправкой сообщения в Telegram;
- Проект ранее был развернут на сервере: <https://myfoodgramnym.hopto.org/recipes>

### Развертывание на локальном сервере

1. Установите на сервере `docker` и `docker-compose`.
2. Создайте файл `.env`. Шаблон для заполнения файла нахоится в `/infra/.env.example`.
3. Выполните команду `docker-compose up -d --buld`.
4. Выполните миграции `docker-compose exec backend python manage.py migrate`.
5. Создайте суперюзера `docker-compose exec backend python manage.py createsuperuser`.
6. Соберите статику `docker-compose exec backend python manage.py collectstatic --no-input`.
7. **Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.**
8. Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>.
9. Заполните базу ингредиентами через администрациооную пнель <<http://localhost/admin>

### Импорт CSV  файлов осуществляется через панель админку
1. Заходиv в раздел Ингредиенты
2. Кликаем на Импорт
3. Выбираем CSV файл
4. Кликаем на загрузку


## 🛠 Стек технологий
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)


# Ресурсы API Foodgram

**AUTH**: получение/удаление токена авторизации.

**USERS**: пользователи: регистрация, просмотр/изменение личного профиля, просмотр пользовательских профилей, подписка/отписка на пользователей.

**TAGS**: теги категории рецептов (создаются и редактируюся пользователями с правами администратора). Описывается полями:
```sh
- Название.
- Цветовой HEX-код (например, #49B64E).
- Slug.
```

**RECIPES**: рецепты. У каждого авторизованного пользователя есть возможность добавлять рецепт в "Избранное" и в "Список покупок".
Каждый рецепт содержит следующие поля:
```sh
- Автор публикации (пользователь).
- Название.
- Картинка.
- Текстовое описание.
- Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
- Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
- Время приготовления в минутах.
```

**INGREDIENTS**: ингредиенты.
Поля:
```sh
- Название.
- Количество.
- Единицы измерения.
```

# Пользовательские роли

**Права анонимного пользователя:**
- Создание аккаунта.
- Просмотр: рецепты на главной, отдельные страницы рецептов, страницы пользователей.
- Фильтрация рецептов по тегам.

**Права авторизованного пользователя (USER):**
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

**Права администратора (ADMIN):**
Все права авторизованного пользователя +
- Изменение пароля любого пользователя,
- Создание/блокирование/удаление аккаунтов пользователей,
- Редактирование/удаление любых рецептов,
- Добавление/удаление/редактирование ингредиентов.
- Добавление/удаление/редактирование тегов.

**Администратор Django** — те же права, что и у роли Администратор.

### Алгоритм регистрации пользователей

Для добавления нового пользователя нужно отправить POST-запрос на эндпоинт:

```
POST /api/users/
```

- В запросе необходимо передать поля:

1. ```email``` - (string) почта пользователя;
2. ```username``` - (string) уникальный юзернейм пользователя;
3. ```first_name``` - (string) имя пользователя;
4. ```last_name``` - (string) фамилия пользователя;
5. ```password``` - (string) пароль пользователя.

Пример запроса:

```sh
{
"email": "vpupkin@yandex.ru",
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин",
"password": "Qwerty123"
}
```

Далее необходимо получить авторизационный токен, отправив POST-запрос на эндпоинт:

```
POST /api/auth/token/login/
```

- В запросе необходимо передать поля:

1. ```password``` - (string) пароль пользователя;
2. ```email``` - (string) почта пользователя.

Пример запроса:

```sh
{
"password": "Qwerty123",
"email": "vpupkin@yandex.ru"
}
```

Пример ответа:

```sh
{
  "auth_token": "string"
}
```

Поученный токен всегда необходимо передавать в заголовке (```Authorization: Token TOKENVALUE```) для всех запросов, которые требуют авторизации.

### Изменение пароля текущего пользователя:

```
POST /api/users/set_password/
```

Пример запроса:

```sh
{
  "new_password": "string",
  "current_password": "string"
}
```

### Удаление токена пользователя:

```
POST /api/auth/token/logout/
```

### Регистрация пользователей админом

Пользователя может создать администратор через админ-зону сайта. Получение токена осуществляется способом, описанным выше.

### Примеры использования API для неавторизованных пользователей:

Для неавторизованных пользователей работа с API доступна в режиме чтения.

```sh
GET /api/users/- получить список всех пользователей.
GET /api/tags/- получить список всех тегов.
GET /api/tags/{id}/ - получить тег по ID.
GET /api/recipes/- получить список всех рецептов.
GET /api/recipes/{id}/ - получить рецепт по ID.
GET /api/users/subscriptions/ - получить список всех пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.
GET /api/ingredients/ - получить список ингредиентов с возможностью поиска по имени.
GET /api/ingredients/{id}/ - получить ингредиент по ID.
```

#### Пример GET-запроса:
```
GET /api/recipes/
```

#### Пример ответа:
- код ответа сервера: 200 OK
- тело ответа:

```sh
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

#### Пример GET-запроса с фильтрацией по наименованию:
```
GET /api/ingredients/?name=абри
```

#### Пример ответа:
- код ответа сервера: 200 OK
- тело ответа:

```sh
[
    {
        "id": 1,
        "name": "абрикосовое варенье",
        "measurement_unit": "г"
    },
    ...
        {
        "id": 6,
        "name": "абрикосы консервированные",
        "measurement_unit": "г"
    }
]
```

#### Пример POST-запроса:
```
POST /api/recipes/
```
Авторизация по токену.
Запрос от имени пользователя должен выполняться с заголовком "Authorization: Token TOKENVALUE"

```sh
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

#### Пример ответа:
- код ответа сервера: 201
- тело ответа:

```sh
{
"id": 0,
"tags": [
{}
],
"author": {
"email": "user@example.com",
"id": 0,
"username": "string",
"first_name": "Вася",
"last_name": "Пупкин",
"is_subscribed": false
},
"ingredients": [
{
"id": 0,
"name": "Картофель отварной",
"measurement_unit": "г",
"amount": 1
}
],
{
"is_favorited": true,
"is_in_shopping_cart": true,
"name": "string",
"image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
"text": "string",
"cooking_time": 1
}
```

***
## Автор

-Варламов Николай [@Devarlamov](https://www.github.com/devarlamov)

