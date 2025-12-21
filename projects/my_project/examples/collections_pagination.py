from typing import List, TypeVar

T = TypeVar('T')

def paginate(items: List[T], page: int, per_page: int) -> List[T]:
    """Безопасная пагинация."""
    if page < 1 or per_page < 1:
        return []
    start = (page - 1) * per_page
    return items[start:start + per_page]

# Пример
if __name__ == "__main__":
    data = list(range(1, 101))  # 100 элементов
    print("Стр. 1:", paginate(data, 1, 10))  # [1..10]
    print("Стр. 2:", paginate(data, 2, 10))  # [11..20]