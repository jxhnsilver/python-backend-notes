## Основное назначение

Командная утилита для управления Django-проектом. Создается автоматически при создании проекта.
## Базовая структура файла
```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(...)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
```
## Основные команды

### Разработка и запуск
```bash
# Запуск сервера разработки
python manage.py runserver
python manage.py runserver 8000           # На порту 8000
python manage.py runserver 0.0.0.0:8000   # Доступ с других устройств

# Проверка кода
python manage.py check                    # Проверка конфигурации
python manage.py check --deploy          # Проверка для продакшена
```
### База данных
```python
# Миграции
python manage.py makemigrations          # Создание миграций
python manage.py makemigrations app_name # Для конкретного приложения
python manage.py migrate                 # Применение миграций
python manage.py migrate app_name        # Миграции приложения
python manage.py showmigrations          # Показать все миграции
python manage.py sqlmigrate app 0001    # Показать SQL миграции

# Работа с БД
python manage.py dbshell                 # Открыть оболочку БД
python manage.py flush                   # Очистить БД (удалить все данные)
```
### Администратор и пользователи
```bash
# Создание суперпользователя
python manage.py createsuperuser

# Управление пользователями
python manage.py changepassword username # Сменить пароль
python manage.py shell                   # Django shell (Python с доступом к БД)
```
### Статические файлы
```bash
python manage.py collectstatic          # Собрать статику для продакшена
python manage.py findstatic css/style.css # Найти статический файл
```
## Полезные команды

### Отладка и информация
```bash
python manage.py shell_plus             # Улучшенный shell (django-extensions)
python manage.py show_urls              # Показать все URL
python manage.py sqlflush               # Показать SQL для очистки БД
python manage.py diffsettings           # Показать отличия от дефолтных настроек
```
### Тестирование
```bash
python manage.py test                   # Запустить все тесты
python manage.py test app_name          # Тесты приложения
python manage.py test app_name.tests    # Конкретный тестовый модуль
python manage.py test --keepdb          # Сохранить тестовую БД
python manage.py test --parallel        # Параллельное выполнение
```
### Приложения
```bash
# Создание приложения
python manage.py startapp app_name

# Переводы
python manage.py makemessages          # Создать файлы перевода
python manage.py compilemessages       # Скомпилировать переводы
```
## Примеры использования

### Стандартный workflow
```bash
# Создать проект
django-admin startproject myproject
cd myproject

# Создать приложение
python manage.py startapp blog

# Настроить models.py, добавить приложение в settings.py

# Создать и применить миграции
python manage.py makemigrations blog
python manage.py migrate

# Создать администратора
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```
## Важные особенности

1. **manage.py** автоматически устанавливает переменную окружения `DJANGO_SETTINGS_MODULE`
2. Требует корректной структуры проекта
3. Работает только из корневой директории проекта
4. Все команды выполняются в контексте Django