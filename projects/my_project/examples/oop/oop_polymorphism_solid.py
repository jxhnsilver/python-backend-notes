from abc import ABC, abstractmethod
from typing import List

class PaymentProcessor(ABC):
    """Интерфейс для всех платёжных систем — Принцип подстановки Барбары Лисков (LSP)"""
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class StripeProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f"[Stripe] Обработка {amount} руб.")
        return True

class PayPalProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f"[PayPal] Обработка {amount} руб.")
        return True

class OrderService:
    """
    Зависит от абстракции, а не от конкретной реализации —
    Принцип инверсии зависимостей (DIP).
    """
    def __init__(self, payment_processor: PaymentProcessor):
        self._processor = payment_processor

    def checkout(self, amount: float) -> bool:
        return self._processor.process(amount)

# Использование
if __name__ == "__main__":
    order1 = OrderService(StripeProcessor())
    order1.checkout(1000.0)

    order2 = OrderService(PayPalProcessor())
    order2.checkout(1000.0)