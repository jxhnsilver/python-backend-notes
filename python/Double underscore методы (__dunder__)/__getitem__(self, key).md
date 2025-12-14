Позволяет использовать объект как **контейнер**: `obj[key]`.

### Когда используется

- При создании кастомных списков, маппингов,
- Для поддержки итерации (если есть `__len__`).
```python
class UserRegistry:
    def __init__(self, users):
        self._users = {u.user_id: u for u in users}

    def __getitem__(self, user_id: str):
        return self._users[user_id]

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

registry = UserRegistry([
    User("U1", "Илья"),
    User("U2", "Анна")
])

print(registry["U1"].name)  # → Илья
```
### Нюансы

- Может вызываться при итерации (`for x in obj`), если нет `__iter__`.
- Поддерживает срезы, если обработать `isinstance(key, slice)`.