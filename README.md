# Проект YaMDb

## Описание проекта
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Стек, использованный при написании проекта
- Python 3.7
- Django 2.2.28
- DRF
- JWT

## Запуск проекта в dev-режиме
- Склонируйте репозиторий:
git clone git@github.com:Pascal-163/YaMDb.git

- Установите и активируйте виртуальное окружение:
cd api_yamdb/
python -m venv venv
source venv/Scripts/activate

- Установите зависимости из файла requirements.txt:
pip install -r requirements.txt

- Примените миграции:
python api_yamdb/manage.py migrate

- Запустите проект:
python api_yamdb/manage.py runserver

- Заполните тестовые данные из папки api_yamdb/static/data:
python api_yamdb/manage.py import_csv

## Примеры нескольких запросов к нашему API:

- Получение пользователя по username

''' http://127.0.0.1:8000/api/v1/users/{username}/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}'''

- Добавление новой категории
http://127.0.0.1:8000/api/v1/categories/
{
  "name": "string",
  "slug": "string"
}

- Удаление жанра
http://127.0.0.1:8000/api/v1/genres/{slug}/

- Получение списка всех произведений
http://127.0.0.1:8000/api/v1/titles/
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}

- Добавление нового отзыва
http://127.0.0.1:8000/api/v1/genres/{slug}/
{
  "text": "string",
  "score": 1
}

- Частичное обновление комментария к отзыву
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
{
  "text": "string"
}

- Все запросы к этому API хранятся в документации, которая станет доступна после запуска проекта по адресу:
http://127.0.0.1:8000/redoc/


## Авторы проекта
Аксёнов Даниил разработчик 1-Teamlead (управление пользователями)
Шатилова Ольга разработчик 2 (модели, view, эндпоинты)
Сидоров Алексей - разработчик 3 (отзывы, комментарии, рейтинг) 
Telegram @pascal161   
aleksid92@gmail.com
