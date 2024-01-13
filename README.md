# Проект "YaMDb"

Добро пожаловать в наш проект **YaMDb**! 

## О проекте

Проект "YaMDb" предоставляет платформу для пользовательских отзывов на различные произведения. Произведения подразделяются на категории: "Книги", "Фильмы", "Музыка", и список категорий может быть расширен.

Само содержание произведений не хранится в проекте, поэтому здесь нельзя просмотреть фильмы или послушать музыку. В каждой категории существуют различные произведения, такие как книги, фильмы или музыка. Каждому произведению может быть присвоен жанр из предварительно заданных вариантов, таких как "Фантастика", "Рок" или "Классика". Новые жанры могут создавать только администраторы.

Пользователи могут оставлять текстовые отзывы и выставлять рейтинг произведению. Они также могут комментировать отзывы других пользователей и ставить им оценки.

## Доступный функционал

Для работы с проектом доступны следующие ресурсы API:

- **Аутентификация (AUTH)**: процесс проверки подлинности пользователя.
- **Пользователи (USERS)**: информация о зарегистрированных пользователях.
- **Произведения (TITLES)**: информация о произведениях, на которые пишут отзывы (фильмы, книги, музыка).
- **Категории (CATEGORIES)**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").
- **Жанры (GENRES)**: информация о жанрах произведений. Одно произведение может быть связано с несколькими жанрами.
- **Отзывы (REVIEWS)**: отзывы на произведения. Каждый отзыв связан с определенным произведением.
- **Комментарии (COMMENTS)**: комментарии к отзывам. Каждый комментарий связан с определенным отзывом.

Алгоритм регистрации пользователей включает следующие шаги:

1. Пользователь отправляет POST-запрос с параметром email на `/api/v1/auth/email/`.
2. Платформа отправляет письмо с кодом подтверждения (confirmation_code) на адрес электронной почты пользователя (функция в разработке).
3. Пользователь отправляет POST-запрос с параметрами email и confirmation_code на `/api/v1/auth/token/`. В ответе на запрос пользователю приходит токен (JWT-токен).

Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.

В проекте предусмотрены следующие пользовательские роли:

- **Анонимный пользователь (Anonymous)**: может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (User)**: имеет все права анонимного пользователя, а также может публиковать отзывы, ставить рейтинг произведениям, комментировать отзывы других пользователей, редактировать и удалять свои отзывы и комментарии.
- **Модератор (Moderator)**: имеет те же права, что и аутентифицированный пользователь, плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор (Administrator)**: обладает полными правами на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры, а также назначать роли другим пользователям.
- **Администратор Django (Django Administrator)**: имеет те же права, что и роль Администратор.

## Как запустить проект

Для установки проекта необходимо выполнить следующие шаги:

1. Склонировать репозиторий.
2. Находясь в папке с кодом, создать виртуальное окружение с помощью команды `python -m venv venv` и активировать его (Windows: `source venv\scripts\activate`; Linux/Mac: `source venv/bin/activate`).
3. Установить необходимые зависимости с помощью команды `python -m pip install -r requirements.txt`.
4. Заполнить базу данных из файлов csv: `python manage.py from_csv_to_db`

Для запуска сервера разработки необходимо выполнить следующие команды в директории проекта:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Документация к API доступна по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) после запуска сервера с проектом

После выполнения этих шагов проект будет запущен и станет доступен по адресу [localhost:8000](http://localhost:8000/).

#### Надеемся, вам у нас понравится!

---

Если у вас возникнут вопросы, пожелания и предложения, вы можете обращаться к авторам этого проекта. Присылайте ваши письма на наш почтовый адрес __*www.yamdb@yandex.com*__. Будем рады видеть вашу обратную связь! 

