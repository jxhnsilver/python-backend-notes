from typing import List, Dict, Any

def flatten_orders(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Пример: расплющить заказы с вложенными товарами в плоский список.
    Бывает при экспорте в CSV или аналитике.
    """
    result = []
    for order in orders:
        for item in order.get("items", []):
            result.append({
                "order_id": order["id"],
                "user_id": order["user_id"],
                "item_name": item["name"],
                "item_price": item["price"],
                "item_quantity": item["qty"],
            })
    return result

# Пример
if __name__ == "__main__":
    orders = [
        {
            "id": 1,
            "user_id": "U1",
            "items": [
                {"name": "Laptop", "price": 50000, "qty": 1},
                {"name": "Mouse", "price": 1000, "qty": 2},
            ],
        }
    ]
    flat = flatten_orders(orders)
    for row in flat:
        print(row)