«Официальное» строковое представление объекта для **разработчика**.

### Когда используется

- В отладчике, REPL, логах,
- При вызове `repr(obj)` или `logging`.
```python
class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, name={self.name!r})"

user = User("U1001", "Илья")
print(repr(user)) # User(user_id='U1001', name='Илья')
```
### Нюансы

- Должен быть **однозначным** и, по возможности, **воспроизводимым** (`eval(repr(obj)) == obj`).
- Используй `!r` в f-строках — это вызовет `repr()` для значений.