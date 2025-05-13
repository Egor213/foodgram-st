## Клонирование проекта

Клонируйте репозиторий на вашу локальную машину:

```sh
git clone https://github.com/Egor213/foodgram-st.git
````

После выполнения этой команды появится директория `foodgram-st`, содержащая весь проект.

---

## Запуск проекта

Перейдите в директорию `infra`:

```sh
cd foodgram-st/infra
```

Создайте файл `.env` на основе примера:

```sh
cp .env.example .env
```

Пример содержимого `.env`:

```env
DJANGO_SECRET_KEY=secret-kEy
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost
CORS_ALLOWED_HOSTS=http://localhost:3000
NGINX_PORT=80
DB_ENGINE=postgresql
DB_NAME=test
DB_PASSWORD=test
DB_USER=test
DB_HOST=db
DB_PORT=5432
```

Запустите контейнеры:

```sh
docker compose up -d --build
```

Вы должны увидеть запуск всех необходимых сервисов. Проверить их можно с помощью команды:

```sh
docker ps
```



---

## Доступ к приложению

Приложение будет доступно по адресу:

**[http://localhost](http://localhost)**

---

## Демо-аккаунты

### Администратор

* **Email**: `admin@example.com`
* **Пароль**: `adminpass`

### Обычные пользователи

| Email                                           | Пароль    |
| ----------------------------------------------- | --------- |
| [tolick@gmail.com](mailto:tolick@gmail.com)     | superpass |
| [vitalick@gmail.com](mailto:vitalick@gmail.com) | superpass |
| [nikitos@gmail.com](mailto:nikitos@gmail.com)   | superpass |

---

##  Сценарий работы


* Пользователь может **войти** на сайт.
* Пользователь может **зарегистрироваться**.
* Залогиненный пользователь может **сменить пароль**.


* Главная страница содержит **список всех рецептов**, отсортированных по дате.
* Пользователь может **создавать рецепты**.
* Можно **просматривать подробности** рецептов.
* Пользователь может **подписываться на других** и просматривать свои подписки.


* Можно добавлять рецепты в **избранное**.
* Можно добавлять рецепты в **список покупок** и **скачивать его в PDF**.


---

##  Остановка проекта

Чтобы остановить и удалить все контейнеры и тома, выполните:

```sh
docker compose down -v
```

---

## Стек технологий

* Python / Django / Django REST Framework
* PostgreSQL
* Docker / Docker Compose
* Gunicorn / Nginx
* FPDF (для формирования PDF файла)
* React (для фронтенда)
