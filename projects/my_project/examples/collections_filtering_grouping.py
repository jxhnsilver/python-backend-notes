from typing import List, Dict, Any
from collections import defaultdict

def get_active_users(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация: только активные пользователи."""
    return [u for u in users if u.get("is_active", False)]

def group_users_by_country(users: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Группировка: пользователи по странам."""
    groups = defaultdict(list)
    for user in users:
        country = user.get("country", "unknown")
        groups[country].append(user["name"])
    return dict(groups)

# Пример
if __name__ == "__main__":
    users = [
        {"name": "Илья", "country": "RU", "is_active": True},
        {"name": "Анна", "country": "RU", "is_active": False},
        {"name": "John", "country": "US", "is_active": True},
    ]
    print("Активные:", [u["name"] for u in get_active_users(users)])
    print("По странам:", group_users_by_country(users))