## Основное назначение

Конфигурационный файл Django-проекта, содержащий все настройки приложения. Создается автоматически командой `django-admin startproject`.
## Структура файла (основные секции)
```python
# 1. Безопасность
SECRET_KEY = 'ваш-секретный-ключ'  # Никогда не коммитьте в Git!
DEBUG = True  # Только для разработки!

# 2. Разрешенные хосты
ALLOWED_HOSTS = []  # При DEBUG=True может быть пустым

# 3. Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Ваши приложения добавляются сюда
]

# 4. Базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite по умолчанию
        'NAME': BASE_DIR / 'db.sqlite3',  # Для продакшена - PostgreSQL/MySQL
    }
}

# 5. Маршрутизация URL
ROOT_URLCONF = 'myproject.urls'

# 6. Шаблоны (HTML)
TEMPLATES = [ ... ]

# 7. Middleware (посредники)
MIDDLEWARE = [ ... ]

# 8. Статические файлы (CSS, JS, картинки)
STATIC_URL = '/static/'
```

| Настройка                        | Описание                                                                      |
| -------------------------------- | ----------------------------------------------------------------------------- |
| `DEBUG = True/False`             | Режим отладки. **Всегда `False` в продакшене!**                               |
| `ALLOWED_HOSTS`                  | Список доменов, с которых разрешён доступ к сайту (в продакшене обязателен).  |
| `INSTALLED_APPS`                 | Список всех подключённых приложений (встроенных и своих, например `'myapp'`). |
| `MIDDLEWARE`                     | Цепочка обработчиков запросов/ответов (авторизация, сессии, CSRF и т.д.).     |
| `DATABASES`                      | Конфигурация подключения к БД (по умолчанию — SQLite).                        |
| `TEMPLATES`                      | Настройки шаблонизатора (папки, контекст-процессоры).                         |
| `STATIC_URL`, `STATICFILES_DIRS` | Пути к статическим файлам (CSS, JS, изображения).                             |
| `SECRET_KEY`                     | Секретный ключ для шифрования (никогда не коммить в Git!).                    |
## Обязательные действия
### 1. После создания приложения
```bash
python manage.py startapp myapp
```
Добавить в `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'myapp',
]
```
### 2. Перед продакшеном
```python
DEBUG = False
ALLOWED_HOSTS = ['ваш-домен.com', 'IP-адрес']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Использовать переменные окружения
```
### 3. Смена базы данных
```python
# Для PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
## Структура каталогов проекта
```text
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py  # <-- Этот файл
│   ├── urls.py
│   └── wsgi.py
└── myapp/
    ├── __init__.py
    ├── models.py
    └── views.py
```
## Команды после изменений
```bash
# После добавления приложения
python manage.py makemigrations
python manage.py migrate

# После настройки статики (продакшен)
python manage.py collectstatic
```
## Переменные окружения (рекомендуемый подход)
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-key-только-для-разработки')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
```
## Важные моменты

1. `SECRET_KEY` должен оставаться секретным
2. `DEBUG=True` показывает детали ошибок, но опасен в продакшене
3. Каждое новое приложение нужно добавлять в `INSTALLED_APPS`
4. `ALLOWED_HOSTS` должен содержать разрешенные домены
5. Настройки базы данных зависят от окружения