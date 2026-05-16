# HomeworkDRF - Habit Tracker API

Бэкенд-часть приложения для управления привычками с интеграцией Telegram-бота и отложенными задачами.

## 📋 О проекте

Приложение помогает пользователям формировать полезные привычки и отслеживать их выполнение. Пользователи могут создавать привычки, указывать время и место выполнения, получать напоминания в Telegram. Проект полностью контейнеризирован с использованием Docker и имеет CI/CD pipeline через GitHub Actions.

## 🛠 Технологии

- **Python** 3.12
- **Django** 5.1
- **Django REST Framework** 3.15
- **PostgreSQL** - база данных
- **Redis** - брокер для Celery
- **Celery** - отложенные задачи
- **Celery Beat** - периодические задачи
- **JWT** - аутентификация
- **Telegram Bot API** - отправка уведомлений
- **Gunicorn** - production сервер
- **Nginx** - reverse proxy
- **Docker / Docker Compose** - контейнеризация
- **GitHub Actions** - CI/CD

## 📁 Структура проекта
homeworkdrf/
├── .github/
│ └── workflows/
│ └── deploy.yml # CI/CD pipeline
├── config/ # Настройки проекта
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── celery.py
├── users/ # Приложение пользователей
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py
│ ├── urls.py
│ ├── views.py
│ └── tests.py
├── materials/ # Приложение материалов
├── services/ # Сервисы
├── .env # Переменные окружения (не в git)
├── .env.example # Пример переменных окружения
├── .gitignore # Игнорируемые файлы
├── docker-compose.yml # Docker Compose конфигурация
├── Dockerfile # Docker образ
├── nginx.conf # Nginx конфигурация
├── requirements.txt # Python зависимости
├── pyproject.toml # Poetry конфигурация
├── poetry.lock # Lock файл зависимостей
└── README.md # Документация

text

## 🚀 Установка и запуск

### Требования

- Docker Desktop (Windows/Mac) или Docker Engine (Linux)
- Docker Compose v2
- Git

### 1. Клонирование репозитория

```bash
git clone https://github.com/AntonSmolyaninov/HomeWorkDRF.git
cd HomeWorkDRF
2. Настройка переменных окружения
Скопируйте .env.example в .env и заполните значения:

bash
cp .env.example .env
3. Запуск приложения
bash
# Собрать и запустить контейнеры
docker compose up -d --build

# Применить миграции
docker compose exec web python manage.py migrate

# Создать суперпользователя
docker compose exec web python manage.py createsuperuser

# Собрать статические файлы
docker compose exec web python manage.py collectstatic --noinput
4. Проверка работы
bash
# Проверить статус контейнеров
docker compose ps

# Просмотреть логи
docker compose logs -f

# Проверить healthcheck
curl http://localhost:8000/health/
5. Остановка
bash
docker compose down

# Остановка с удалением volumes
docker compose down -v
📚 API Эндпоинты
Аутентификация
Метод	Эндпоинт	Описание
POST	/api/auth/register/	Регистрация
POST	/api/auth/token/	Получение JWT токена
POST	/api/auth/token/refresh/	Обновление JWT токена
Привычки
Метод	Эндпоинт	Описание
GET	/api/habits/	Список привычек (свои + публичные)
POST	/api/habits/	Создание привычки
GET	/api/habits/{id}/	Детали привычки
PUT	/api/habits/{id}/	Обновление привычки
DELETE	/api/habits/{id}/	Удаление привычки
GET	/api/habits/my/	Только мои привычки
GET	/api/habits/public/	Публичные привычки
Пагинация
По умолчанию вывод 5 привычек на страницу. Параметры запроса:

page - номер страницы

page_size - количество на странице (max 20)

📖 Документация API
После запуска сервера документация доступна по адресам:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

🔧 Команды для управления
bash
# Просмотр логов всех сервисов
docker compose logs -f

# Просмотр логов конкретного сервиса
docker compose logs web -f
docker compose logs celery_worker -f
docker compose logs celery_beat -f

# Перезапуск сервиса
docker compose restart web
docker compose restart celery_worker celery_beat

# Выполнение команд в контейнере
docker compose exec web python manage.py shell
docker compose exec web python manage.py dbshell

# Очистка Docker
docker system prune -a -f
🔐 Переменные окружения
Создайте файл .env на основе .env.example:

env
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=django_drv
DB_USER=postgres
DB_PASSWORD=change_me
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

TELEGRAM_BOT_TOKEN=your_bot_token_here

STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_HOST_USER=your_email@yandex.ru
EMAIL_HOST_PASSWORD=your_password
DEFAULT_FROM_EMAIL=your_email@yandex.ru
🤖 GitHub Actions CI/CD
При каждом push в ветку main автоматически запускается pipeline:

Тесты - запуск pytest с покрытием 80%+

Линтеры - flake8, black, isort, mypy

Сборка - Docker образ

Деплой - автоматическое развертывание на сервер

Проверка статуса workflow
bash
# Через GitHub CLI (если установлен)
gh run list

# Или через браузер
# Перейдите в репозиторий → Actions
🧪 Тестирование
bash
# Запуск всех тестов
docker compose exec web pytest

# Запуск с покрытием
docker compose exec web pytest --cov=habits --cov=users --cov-report=term

# Запуск конкретного теста
docker compose exec web pytest habits/tests.py::HabitModelTest
📝 Лицензия
Учебный проект. Не предназначен для коммерческого использования.

👤 Автор
Антон Смольянинов

GitHub: AntonSmolyaninov

Email: anton1985smolyaninov@yandex.ru
