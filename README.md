# HomeworkDRF - Habit Tracker API

Бэкенд-часть приложения для управления привычками с интеграцией Telegram-бота и отложенными задачами.

## Технологии

- Python 3.12
- Django 5.1
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Docker / Docker Compose

## Требования

- Docker Desktop (Windows/Mac) или Docker Engine (Linux)
- Docker Compose v2

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/homeworkdrf.git
cd homeworkdrf
2. Настройка переменных окружения
Скопируйте .env.example в .env и заполните значения:

bash
cp .env.example .env
Обязательные переменные:

SECRET_KEY - секретный ключ Django

DB_PASSWORD - пароль PostgreSQL

TELEGRAM_BOT_TOKEN - токен Telegram бота

3. Запуск приложения
bash
# Собрать и запустить контейнеры
docker compose up --build -d

# Применить миграции
docker compose exec web python manage.py migrate

# Создать суперпользователя
docker compose exec web python manage.py createsuperuser
4. Остановка
bash
docker compose down
API Эндпоинты
Метод	Эндпоинт	Описание
POST	/api/auth/register/	Регистрация
POST	/api/auth/token/	Получение JWT
POST	/api/auth/token/refresh/	Обновление JWT
GET	/api/habits/	Список привычек
POST	/api/habits/	Создание привычки
GET	/api/habits/my/	Мои привычки
GET	/api/habits/public/	Публичные привычки
PUT	/api/habits/{id}/	Обновление
DELETE	/api/habits/{id}/	Удаление
Документация
Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

Команды для управления
bash
# Просмотр логов
docker compose logs -f

# Перезапуск сервиса
docker compose restart web

# Выполнение команд в контейнере
docker compose exec web python manage.py shell
Структура проекта
text
homeworkdrf/
├── config/           # Настройки проекта
├── users/            # Приложение пользователей
├── materials/        # Приложение материалов
├── services/         # Сервисы
├── .env              # Переменные окружения
├── docker-compose.yml
├── Dockerfile
└── README.md
Лицензия
Учебный проект

text

## Файл `.env.example`

Создайте файл `.env.example` (без реальных значений):

```env
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=django_drv
DB_USER=postgres
DB_PASSWORD=change_me
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

TELEGRAM_BOT_TOKEN=your_bot_token_here

STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_HOST_USER=your_email@yandex.ru
EMAIL_HOST_PASSWORD=your_password
