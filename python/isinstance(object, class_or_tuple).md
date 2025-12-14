Встроенная функция, которая **проверяет, является ли объект экземпляром указанного класса (или одного из классов)**.

### ✅ Зачем нужно?

- Безопасная проверка типа **до** вызова методов,
- Обработка разных типов в полиморфном коде,
- Защита от `AttributeError` и `TypeError`.
```python
isinstance(obj, SomeClass)        → bool
isinstance(obj, (ClassA, ClassB)) → bool (если obj — экземпляр любого из)
```


```python
from typing import Union

def process_data(data: Union[str, list]) -> str:
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, list):
        return ", ".join(str(x) for x in data)
    else:
        raise TypeError("Ожидался str или list")

print(process_data("hello"))      # → HELLO
print(process_data([1, 2, 3]))    # → 1, 2, 3
```
### Важно: `isinstance` учитывает наследование!
```python
class Animal: pass
class Dog(Animal): pass

dog = Dog()
print(isinstance(dog, Animal))  # → True (не только Dog!)
```
### ❌ Не используй `type(obj) is Class` — это ломает полиморфизм!
