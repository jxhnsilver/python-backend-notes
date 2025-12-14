Определяет, **когда два объекта равны** (`==`).

### Когда используется

- При сравнении объектов в тестах,
- В `set`, `dict` (в связке с `__hash__`),
- При фильтрации (`if obj in list`).
```python
class User:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id

user1 = User("U1")
user2 = User("U1")
user3 = User("U2")

print(user1 == user2)  # True
print(user1 == user3)  # False
print(user1 == "U1")   # False (защита от сравнения с другим типом)
```
### Нюансы

- Всегда проверяй тип: `isinstance(other, MyClass)`.
- Если определяешь `__eq__`, **часто нужно определять `__hash__` (для избежания коллизий в хеш-коллекциях**