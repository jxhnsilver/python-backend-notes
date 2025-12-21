from typing import List

class BankAccount:
    """
    Инкапсуляция: внутреннее состояние защищено (поля: balance и _transaction_history),
    изменение только через контролируемые методы.
    """
    def __init__(self, initial_balance: float = 0):
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self._balance = initial_balance
        self._transaction_history: List[float] = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма депозита должна быть положительной")
        self._balance += amount
        self._transaction_history.append(amount)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        self._transaction_history.append(-amount)

    @property
    def balance(self) -> float:
        return self._balance

    def get_transaction_count(self) -> int:
        return len(self._transaction_history)

    def get_transaction_history(self) -> tuple[float, ...]:
        return tuple(self._transaction_history)