# Проект "YaMDb"

Добро пожаловать в наш проект **YaMDb**! 

## О проекте

Проект "YaMDb" предоставляет платформу для пользовательских отзывов на различные произведения. Произведения подразделяются на категории: "Книги", "Фильмы", "Музыка". Список категорий может быть расширен. В каждой категории существуют различные произведения. Само содержание произведений не хранится в проекте, поэтому здесь нельзя посмотреть фильм или послушать музыку. Каждому произведению может быть присвоен жанр из предварительно заданных вариантов, таких как "Фантастика", "Рок" или "Классика". Новые жанры могут создавать только администраторы.

Пользователи могут оставлять текстовые отзывы и выставлять рейтинг произведению. Они также могут комментировать отзывы других пользователей и ставить им оценки.

## Стек технологий

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

## Доступный функционал

Для работы с проектом доступны следующие ресурсы API:

- **Аутентификация (auth)**: процесс проверки подлинности пользователя.
- **Пользователи (users)**: информация о зарегистрированных пользователях.
- **Произведения (titles)**: информация о произведениях, на которые пишут отзывы (фильмы, книги, музыка).
- **Категории (categories)**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").
- **Жанры (genres)**: информация о жанрах произведений. Одно произведение может быть связано с несколькими жанрами.
- **Отзывы (reviews)**: отзывы на произведения. Каждый отзыв связан с определенным произведением.
- **Комментарии (comments)**: комментарии к отзывам. Каждый комментарий связан с определенным отзывом.

#### Алгоритм регистрации пользователей включает следующие шаги:

1. Пользователь отправляет POST-запрос с параметрами "username" и "email" на localhost:8000/api/v1/auth/signup/.
2. Платформа отправляет письмо с кодом подтверждения (confirmation_code) на адрес электронной почты пользователя (функция недоработана, посмотреть шаблон письма и код подтверждения можно в папке api_yamdb/sent_emails).
3. Пользователь отправляет POST-запрос с параметрами "username" и "confirmation_code" на localhost:8000/api/v1/auth/token/. В ответе на запрос пользователю приходит токен (JWT-токен).

Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.

В проекте предусмотрены следующие пользовательские роли:

- **Анонимный пользователь (Anonymous)**: может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (User)**: имеет все права анонимного пользователя, а также может публиковать отзывы, ставить рейтинг произведениям, комментировать отзывы других пользователей, редактировать и удалять свои отзывы и комментарии.
- **Модератор (Moderator)**: имеет те же права, что и аутентифицированный пользователь, а также право удалять и редактировать любые отзывы и комментарии.
- **Администратор (Administrator)**: обладает полными правами на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры, а также назначать роли другим пользователям.

## Как запустить проект

Для установки проекта необходимо выполнить следующие шаги:

1. Склонировать репозиторий.

```bash
git clone git@github.com:eva-shokom/api_yamdb.git
```

2. Находясь в корневой директории проекта, создать виртуальное окружение и активировать его

```bash
python -m venv venv
```

Для Windows:
```bash
source venv/Scripts/activate
```

Для Linux/Mac:
```bash
source venv/bin/activate
```

3. Обновить pip, установить необходимые зависимости

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Перейти в папку api_yamdb
  
```bash
cd api_yambd
```

5. Выполнить миграции и заполнить базу данных из файлов csv

```bash
python manage.py migrate
python manage.py from_csv_to_db
```

6. Запустить сервер

```bash
python manage.py runserver
```

После выполнения этих шагов проект будет запущен и станет доступен по адресу [localhost:8000/api/v1/](http://localhost:8000/api/v1/)

#### Документация к API доступна по адресу [http://localhost:8000/redoc/](http://localhost:8000/redoc/) после запуска сервера с проектом

#### Надеемся, вам у нас понравится!

---

Проект подготовили:
- [eva-shokom](https://github.com/eva-shokom/) - тимлид, координировала действия команды, декомпозировала задачи, отвечала за часть, касающуюся отзывов, комментариев и рейтинга произведений.
- [richckov](https://github.com/richckov/) - писал код для категорий, жанров и произведений, выполнял импорт данных в базу данных из .csv файлов.
- [eXc1t3](https://github.com/eXc1t3/) - реализовал авторизацию и аутентификацию пользователей, права пользователей.

Если у вас возникнут вопросы, пожелания и предложения, вы можете обращаться к авторам этого проекта. Будем рады видеть вашу обратную связь! 

