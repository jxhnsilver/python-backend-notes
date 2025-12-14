Возвращает **хэш-код объекта** — целое число для быстрого сравнения в `set` и `dict`.

### Когда используется

- Когда объект используется как **ключ в словаре** или **элемент множества**.

```python
class User:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __eq__(self, other) -> bool:
        return isinstance(other, User) and self.user_id == other.user_id

    def __hash__(self) -> int:
        return hash(self.user_id)

user1 = User("U1")
user2 = User("U1")

# Теперь можно использовать в set/dict
users = {user1, user2}
print(len(users))  # → 1 (дубликаты не добавляются)

lookup = {user1: "active"}
print(lookup[user2])  # → "active" (работает через __eq__ и __hash__) определил что user1 и user2 равны и вытщил хначение по хешу id
```
### Нюансы

- **Только для неизменяемых объектов!** Если объект меняется — хэш становится некорректным.
- Если определил `__eq__`, **хэш должен зависеть от тех же полей**.
