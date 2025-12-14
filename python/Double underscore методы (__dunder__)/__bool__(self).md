**Магический метод**, который определяет, **как объект ведёт себя в булевом контексте** (`if obj:`, `bool(obj)`, `not obj` и т.д.).

Если не определён — Python использует `__len__()` (если есть):  
→ `len(obj) > 0` → `True`, иначе `False`.  
Если нет ни `__bool__`, ни `__len__` → всегда `True`.

| `isinstance()` | Проверка типа | Перед вызовом методов, обработка разных типов |
| -------------- | ------------- | --------------------------------------------- |
### ✅ Зачем нужно?

- Кастомная логика «пустоты» объекта,
- Удобство использования в условиях без `.is_valid()` или `.empty`.

### Пример: валидный ли объект?
```python
class EmailAddress:
    def __init__(self, email: str):
        self.email = email

    def __bool__(self) -> bool:
        # Простейшая проверка
        return "@" in self.email and "." in self.email.split("@")[-1]

# Использование
addr1 = EmailAddress("ilya@example.com")
addr2 = EmailAddress("bad-email")

if addr1:
    print("Валидный email")  # → Валидный email

if not addr2:
    print("Невалидный email")  # → Невалидный email
```
### Пример: непустая коллекция
```python
class Order:
    def __init__(self, items):
        self.items = items

    def __bool__(self) -> bool:
        return len(self.items) > 0

order = Order([])
if not order:
    print("Заказ пуст")  # → Заказ пуст
```
### ⚠️ Важные правила:

1. **Должен возвращать `bool`** — не `int`, не `str`.
2. **Не вызывай напрямую** — используй `bool(obj)` или условия.
3. **Не перегружай без причины** — только если логика «истинности» нетривиальна.