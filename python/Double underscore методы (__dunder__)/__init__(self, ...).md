Метод инициализации экземпляра. Вызывается **после создания объекта** (для настройки состояния).

### Когда используется

- При создании DTO, моделей, сервисов,
- Для валидации входных данных,
- Инициализации внутренних структур.

```python
from typing import List

class Order:
    def __init__(self, order_id: str, items: List[str]):
        if not order_id:
            raise ValueError("order_id не может быть пустым")
        if not items:
            raise ValueError("Заказ должен содержать хотя бы один товар")
        self.order_id = order_id
        self.items = items.copy()  # защита от мутаций внешнего списка

order = Order("ORD-1001", ["Laptop", "Mouse"])
print(order.items) # ['Laptop', 'Mouse']
```
### Нюансы

- Не возвращает значение (всегда `None`).
- Не создаёт объект — этим занимается `__new__`.
- Всегда вызывается при `ClassName(...)`.