Возвращает «длину» объекта. Вызывается при `len(obj)`.

### Когда используется

- При работе с коллекциями, кастомными контейнерами,
- В API для возврата `count`.

```python
class OrderList:
    def __init__(self, orders):
        self._orders = orders

    def __len__(self) -> int:
        return len(self._orders)

orders = OrderList(["ORD-1", "ORD-2"])
print(len(orders))  # → 2
```
### Нюансы

- Должен возвращать **неотрицательное целое**.
- Часто используется в связке с `__getitem__`.