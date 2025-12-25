**Memcached** — это **высокопроизводительный, распределённый кэш-сервер**, который:

- Хранит данные **только в оперативной памяти (RAM)**
- Работает по принципу **ключ → значение**
- Предназначен **только для кэширования**, **не для хранения данных**
- Используется Facebook, Wikipedia, Twitter и другими для снижения нагрузки на БД
## Как работает?

1. Ты запускаешь **демон Memcached** (отдельный процесс).
2. Он выделяет **фиксированный объём RAM** (например, 64 МБ).
3. Приложение (Django) **подключается к нему** по сети (IP:порт или Unix-сокет).
4. Отправляет команды: `set key value`, `get key`, `delete key`.
5. Memcached **автоматически удаляет старые данные**, когда память заполнена (LRU-алгоритм).
## Как настроить Memcached в Django

### Шаг 1. Установи Memcached (на машине)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install memcached
```
**Запустить/проверить:**
```bash
sudo systemctl start memcached
sudo systemctl status memcached  # должен быть active (running)
```
По умолчанию слушает `127.0.0.1:11211`.
### Шаг 2. Установи Python-драйвер

Django поддерживает два:

|Драйвер|Пакет|Комментарий|
|---|---|---|
|`pymemcache`|`pip install pymemcache`|**Рекомендуется**: чистый Python, легко отлаживать|
|`pylibmc`|`pip install pylibmc`|Быстрее, но требует C-библиотек (`libmemcached-dev`)|
### Настрой `CACHES` в `settings.py`

#### Базовый вариант (локальный сервер):
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}
```
#### Через Unix-сокет (быстрее, если на одной машине):
```python
"LOCATION": "unix:/tmp/memcached.sock"
```
#### Кластер из нескольких серверов:
```python
"LOCATION": [
    "10.0.0.10:11211",
    "10.0.0.11:11211",
    "10.0.0.12:11212",
]
```
→ Memcached **автоматически распределит ключи** между ними (без дублирования!).
## Примеры грамотного кода (для джуниора)

### 1. Кэширование результата функции
```python
from django.core.cache import cache
from .models import Product

def get_popular_products():
    key = "popular_products_v1"
    products = cache.get(key)
    if products is None:
        products = list(
            Product.objects.filter(is_active=True)
            .order_by("-views")[:10]
            .values("id", "name", "price")  # ← только нужные поля!
        )
        cache.set(key, products, timeout=60 * 30)  # 30 минут
    return products
```
> ✅ Хорошо:
> 
> - Возвращаем **список словарей**, а не объекты Django → безопасно для сериализации
> - Чёткий `timeout`
> - Ключ с версией (`_v1`) — легко инвалидировать

### 2. Инвалидация при изменении данных
```python
# models.py или в view после save()
from django.core.cache import cache

def update_product(product_id, data):
    Product.objects.filter(id=product_id).update(**data)
    # Сбросить кэш
    cache.delete("popular_products_v1")
```
### 3. Использование в шаблоне (фрагмент)
```django
{% load cache %}
{% cache 1800 top_banner user.id %}
  <div class="banner">Персональный баннер для {{ user.username }}</div>
{% endcache %}
```
✅ Ключ включает `user.id` — чтобы у каждого свой кэш.
## Особенности и подводные камни
|Особенность|Объяснение|
|---|---|
|**Данные исчезают при перезагрузке**|Memcached — **in-memory**, при падении сервера кэш теряется|
|**Нет персистентности**|Не пытайся использовать как БД или очередь|
|**Ключи — байты, макс. 250 байт**|Не используй длинные или сложные ключи|
|**Значения — до 1 МБ**|Не пытайся кэшировать большие файлы или списки из 10к объектов|
|**Сериализация по умолчанию — pickle**|Избегай кэширования Django-моделей — лучше `dict` или `list`|
|**Нет встроенной аутентификации**|Доступен всем в сети → запускай только в доверенной среде (localhost или внутренняя сеть)|
## Memcached vs Redis (что выбрать?)

| Критерий                       | Memcached             | Redis                                  |
| ------------------------------ | --------------------- | -------------------------------------- |
| Скорость                       | Очень высокая         | Высокая                                |
| Тип данных                     | Только key-value      | Строки, списки, хэши, множества        |
| Кластеризация                  | Встроенная (надёжная) | Требует Redis Cluster                  |
| TTL на запись                  | Да                    | Да                                     |
| Инвалидация по шаблону         | Нет                   | Нет (но есть KEYS — не для продакшена) |
| Использование в новых проектах | Редко                 | Почти всегда                           |