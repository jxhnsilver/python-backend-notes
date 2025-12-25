## Основные методы и когда их использовать

### 1. **`cache.set(key, value, timeout)`**

Сохранить значение в кэш.
```python
cache.set("user_123", {"name": "Alice"}, timeout=300)
```
- `key` — строка (лучше с префиксом и версией: `"v2:user_123"`)
- `value` — любой объект, который можно `pickle` (но **только словари/списки**, не модели!)
- `timeout=0` → не кэшировать, `timeout=None` → кэшировать вечно (**не делай так**)
### 2. **`cache.get(key, default=None)`**
Получить значение. Если нет — вернёт `default`.
```python
profile = cache.get("user_123")
if profile is None:
    profile = fetch_from_db()
    cache.set("user_123", profile, 300)
```
⚠️ **Проблема**: если ты кэшируешь `None` как валидное значение, `get()` не отличит «нет ключа» от «ключ = None».  
✅ Решение — использовать **sentinel**:
```python
_SENTINEL = object()
if cache.get("key", _SENTINEL) is _SENTINEL:
    # ключа точно нет
```
### 3. **`cache.add(key, value, timeout)`**
Сохранить **только если ключа ещё нет**.
```python
# Попытка установить флаг "инициализировано"
if cache.add("migration_done", True, timeout=None):
    run_migration()  # выполнится один раз
```
→ Возвращает `True`, если значение установлено, иначе `False`.
### 4. **`cache.get_or_set(key, default, timeout)`**

Атомарно получить или вычислить и сохранить.
```python
# Хорошо для ленивой инициализации
data = cache.get_or_set(
    "expensive_result",
    lambda: heavy_computation(),  # вызовется только если ключа нет
    timeout=600
)
```
→ Можно передать **callable** (например, `datetime.now`).
## Массовые операции (экономят сетевые вызовы)

| Метод                              | Зачем                                           |
| ---------------------------------- | ----------------------------------------------- |
| `cache.get_many(["a", "b", "c"])`  | Получить несколько ключей **одним запросом**    |
| `cache.set_many({"a": 1, "b": 2})` | Сохранить несколько значений **одним запросом** |
| `cache.delete_many(["a", "b"])`    | Удалить несколько ключей                        |
Особенно важно для **Redis/Memcached** — уменьшает latency (**задержка**).
## Управление временем жизни и удалением

| Метод                    | Действие                                                                  |
| ------------------------ | ------------------------------------------------------------------------- |
| `cache.touch("key", 60)` | Обновить TTL ключа (например, продлить сессию)                            |
| `cache.delete("key")`    | Удалить ключ вручную (при обновлении данных)                              |
| `cache.clear()`          | **Очистить ВЕСЬ кэш** (осторожно! удаляет всё, даже от других приложений) |
## Счётчики: `incr()` и `decr()`
```python
cache.set("views", 0)
cache.incr("views")        # → 1
cache.incr("views", 5)     # → 6
```
⚠️ **Неатомарно** в `LocMemCache` и `FileBasedCache`!  
✅ **Атомарно** в **Redis** и **Memcached** (используют нативные команды `INCR`/`DECR`).
## Практические советы для джуниора

1. **Всегда кэшируй только данные, а не объекты**
```python
# ✅ Хорошо
cache.set("user_123", {"id": 123, "name": "Alice"})

# ❌ Плохо
cache.set("user_123", User.objects.get(id=123))
```
2. **Используй `get_or_set` вместо `get` + `set`** — меньше кода, меньше гонок.
3. **Для массовых операций — `get_many`/`set_many`**, а не цикл.
4. **При изменении данных — вызывай `delete`**
```python
def update_profile(user_id, data):
    User.objects.filter(id=user_id).update(**data)
    cache.delete(f"user_{user_id}")  # инвалидация
```
1. **Не используй `clear()` в продакшене** — только для dev.
## Асинхронная поддержка (если используешь async Django)

Все методы имеют асинхронные аналоги с префиксом `a`:
```python
await cache.aset("key", "value")
data = await cache.aget("key")
```
## Вывод

> **Low-level cache API — это рабочая лошадка кэширования в Django.**
> 
> - `set`/`get` — основа,
> - `get_or_set` — для ленивых вычислений,
> - `get_many`/`set_many` — для эффективности,
> - `incr`/`decr` — для счётчиков,
> - `delete` — для инвалидации.