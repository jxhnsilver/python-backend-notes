# возвращает сумму amount только для заказов со статусом "completed"
# список заказов представлен в виде списка словарей
import datetime


class OrderService:
    def get_total_completed_amount(self, orders: list[dict]) -> int:
        total = 0
        for order in orders:
            if order.get("status") == "completed":
                amount = order.get("amount", 0)
                if isinstance(amount, (int, float)):
                    total += int(amount)

        return total

    def group_orders_by_status(self, orders: list[dict]) -> dict[str, int]:
        """Группирует заказы по статусу и считает количество."""
        groups = {}
        for order in orders:
            status = order.get("status", "unknown")
            groups[status] = groups.get(status, 0) + 1
        return groups


if __name__ == "__main__":
    orders = [
        {"id": 1, "amount": 100, "status": "completed"},
        {"id": 2, "amount": 200, "status": "pending"},
        {"id": 3, "amount": 150, "status": "completed"},
    ]

    order_service = OrderService()
    result = order_service.get_total_completed_amount(orders)
    print(result)
