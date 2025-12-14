«Неофициальное» строковое представление для **пользователя**.

### Когда используется

- При `print(obj)`, `str(obj)`,
- В логах, уведомлениях, отчётах.

```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"

user = User("Илья", "ilya@example.com")
print(str(user)) # Илья <ilya@example.com>
print(user)  # print() вызывает __str__ # Илья <ilya@example.com>
```
### Нюансы

- Если не определён — Python использует `__repr__`.
- Должен быть **понятным**, а не техническим.